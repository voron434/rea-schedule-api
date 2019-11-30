from rest_framework import serializers

from schedule.models import Group, Lesson


class GroupSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    faculty = serializers.StringRelatedField()

    class Meta:
        model = Group
        fields = ['title', 'course', 'faculty', 'updated']


class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Lesson
        fields = [
            'teacher', 'group', 'week',
            'subgroup', 'classroom', 'date',
            'lesson_num', 'title', 'lesson_type', 'updated']
