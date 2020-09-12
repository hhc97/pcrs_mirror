from rest_framework import serializers

from .models import StudentFixitProfile

class StudentFixitProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFixitProfile
        fields = ('id', 'user', 'problem_type', 'problem_id', 'submission_time') 
