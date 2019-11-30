from rest_framework import routers, serializers, viewsets

from schedule.models import Group, Lesson


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['title', 'course', 'updated']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'teacher', 'group', 'week',
            'subgroup', 'classroom', 'date',
            'lesson_num', 'title', 'lesson_type', 'updated']
