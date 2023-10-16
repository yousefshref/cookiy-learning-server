from rest_framework import serializers
from . import models



class SpecialySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialy
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user')
    specialty_name = SpecialySerializer(source='specialty')
    class Meta:
        model = models.UserProfile
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):
    teacher_details = UserSerializer(source='teacher', read_only=True)
    teacher_profile = UserProfileSerializer(source='profile', read_only=True)
    class Meta:
        model = models.Course
        fields = '__all__'


class FavCourseSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course')
    class Meta:
        model = models.FavCourse
        fields = '__all__'


class CourseReviewSerializer(serializers.ModelSerializer):
    studet_details = UserSerializer(source='student')
    studet_profile_details = UserProfileSerializer(source='student_profile')
    class Meta:
        model = models.CourseReview
        fields = '__all__'


class EnrollmmentSerializer(serializers.ModelSerializer):
    course_details = CourseSerializer(source='course')
    teacher_details = UserSerializer(source='teacher')
    class Meta:
        model = models.Enrollmment
        fields = '__all__'
