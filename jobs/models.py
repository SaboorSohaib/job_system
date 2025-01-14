from django.db import models
from django.utils.timezone import now
from django.conf import settings

# Job Model
class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='jobs'
    )  # Link each job to a specific user
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# JobResult Model
class JobResult(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='results')
    output = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Result for {self.job.name}"
