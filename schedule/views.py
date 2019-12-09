import json
from datetime import datetime

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from schedule import serializers
from schedule import models


def get_week():
    current_week = datetime.now().isocalendar()[1]
    return current_week


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def groups_list(request):
    groups = models.Group.objects.all()
    json_stats = serializers.GroupSerializer(groups, many=len(groups) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json"
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def facultys_list(request):
    facultys = models.Faculty.objects.all()
    json_stats = serializers.FacultySerializer(facultys, many=len(facultys) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json"
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_schedule(request):
    group_title = request.GET.get("group")
    try:
        group = models.Group.objects.get(title=group_title)
    except ObjectDoesNotExist:
        raise Http404("Group does not exist")
    lessons = models.Lesson.objects.filter(group=group, week=get_week())
    json_stats = serializers.LessonSerializer(lessons, many=len(lessons) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json"
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def courses_list(request):
    faculty_title = request.GET.get("faculty")
    try:
        faculty = models.Faculty.objects.get(title=faculty_title)
    except ObjectDoesNotExist:
        raise Http404("Faculty does not exist")
    courses_by_faculty = models.Course.objects.filter(faculty=faculty)
    json_stats = serializers.CourseSerializer(courses_by_faculty,
                                              many=len(courses_by_faculty) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json"
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def groups_by_course(request):
    faculty_title = request.GET.get("faculty")
    course_title = request.GET.get("course")
    try:
        faculty = models.Faculty.objects.get(title=faculty_title)
    except ObjectDoesNotExist:
        raise Http404("Faculty does not exist")
    try:
        course = models.Course.objects.get(faculty=faculty, title=course_title)
    except ObjectDoesNotExist:
        raise Http404("Course does not exist")
    groups = models.Group.objects.filter(course=course)
    json_stats = serializers.GroupsByCourse(groups, many=len(groups) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(
        json.dumps(response, ensure_ascii=False),
        content_type="application/json"
    )
