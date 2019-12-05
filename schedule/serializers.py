from rest_framework import serializers

from schedule.models import Group, Lesson, Faculty


class GroupSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    faculty = serializers.StringRelatedField()

    class Meta:
        model = Group
        fields = ['title', 'course', 'faculty', 'updated']


class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    # week = 

    class Meta():
        model = Lesson
        fields = [
            'teacher', 'group', 'week',
            'subgroup', 'classroom', 'date',
            'lesson_num', 'title', 'lesson_type', 'updated']


class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = ['title', 'updated']
