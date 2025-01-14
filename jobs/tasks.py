# tasks.py or a similar file
from jobs.models import Job, JobResult
from django.utils import timezone  # Correct import


def process_job(job_id):
    print(f"Processing job with ID: {job_id}")
    try:
        # Retrieve the job from the database
        job = Job.objects.get(id=job_id)

        # Perform the actual job processing (dummy logic here)
        output = f"Job {job.name} processed successfully."

        # Save the result in the JobResult model
        JobResult.objects.create(
            job=job,
            output=output,
            completed_at=timezone.now()
        )

        # Update the job status
        job.status = "completed"
        job.save()

    except Exception as e:
        job.status = "failed"
        job.save()
        JobResult.objects.create(
            job=job,
            output="",
            error_message=str(e),
            completed_at=timezone.now()
        )
        
