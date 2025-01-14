
from rest_framework import serializers
from .models import Job, JobResult
from datetime import datetime
from pytz import UTC

class JobSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')  
    class Meta:
        model = Job
        fields = ['id', 'user', 'name', 'description', 'created_at', 'scheduled_time', 'status', 'result']
        read_only_fields = ['id', 'created_at', 'status', 'result']

    def validate_scheduled_time(self, value):
    # Get the current time (naive datetime, no timezone info)
        now = datetime.now()  # Current time without timezone info (naive)

        # If 'value' (scheduled_time) is timezone-aware, remove the timezone info to make it naive
        if value.tzinfo is not None:
            value = value.replace(tzinfo=None)
        
        # Compare the naive datetime values
        if value < now:
            raise serializers.ValidationError("The scheduled time cannot be in the past.")
        
        return value

    

class JobResultSerializers(serializers.ModelSerializer): 
    job_name = serializers.ReadOnlyField(source='job.id') 
    class Meta: 
        model = JobResult
        fields = ['id', 'job', 'job_name', 'output', 'error_message', 'completed_at']
        read_only_fields = ['id', 'completed_at']