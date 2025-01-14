# from arrow import now
from rest_framework import generics
from .models import Job, JobResult
from .serializers import JobSerializers, JobResultSerializers
from rest_framework.permissions import IsAuthenticated
from jobs.tasks import process_job
from django.utils.timezone import make_aware ,now
from rq import Queue
from redis import Redis

# Job Views
class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save the job instance
        job = serializer.save(user=self.request.user)

        try:
            scheduled_time = job.scheduled_time

            # Ensure scheduled_time is aware
            if scheduled_time.tzinfo is None:
                scheduled_time = make_aware(scheduled_time)

            # Prevent scheduling jobs in the past
            if scheduled_time < now():
                raise ValueError("Scheduled time must be in the future.")

            # Connect to Redis
            redis_conn = Redis()

            # Get the default queue
            queue = Queue(connection=redis_conn)

            # Enqueue the job
            job_enqueued = queue.enqueue_at(scheduled_time, process_job, job.id)
            return job_enqueued
        except Exception as e:
            job.delete()
            raise ValueError(f"Failed to enqueue job: {str(e)}")



class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

# JobResult Views
class JobResultListView(generics.ListAPIView):
    serializer_class = JobResultSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobResult.objects.filter(job__user=self.request.user)

class JobResultDetailView(generics.RetrieveAPIView):
    serializer_class = JobResultSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobResult.objects.filter(job__user=self.request.user)
    