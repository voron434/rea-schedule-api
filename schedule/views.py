import json


from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from schedule import serializers
from schedule import models

from datetime import datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_week():
    current_week = datetime.now().isocalendar()[1]
    return current_week


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def groups_list(request):
    groups = models.Group.objects.all()
    json_stats = serializers.GroupSerializer(groups, many=len(groups) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
    # return JsonResponse(response, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def facultys_list(request):
    facultys = models.Faculty.objects.all()
    json_stats = serializers.FacultySerializer(facultys, many=len(facultys) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_shedule(request):
    """
    Отдать расписание на текущую неделю по имени группы
    """
    try:
        group = request.GET.get("group")
        group_id = models.Group.objects.values_list('id', flat=True).filter(title = group).get()
        lessons = models.Lesson.objects.filter(group = group_id, week = get_week())
    except ObjectDoesNotExist:
        raise Http404()
    

    json_stats = serializers.LessonSerializer(lessons, many=len(lessons) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def courses_list(request):
    
    try:
        faculty_name = request.GET.get("faculty")
        faculty = models.Faculty.objects.filter(title = faculty_name).get()
        course = models.Course.objects.filter(faculty = faculty)
        json_stats = serializers.CourseSerializer(course, many=len(course) > 1).data
        response = {'success': True, 'stats': json_stats}
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
        
    except ObjectDoesNotExist:
        raise Http404()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def groups_by_course(request):
    try:
        faculty_name = request.GET.get("faculty")
        course = request.GET.get("course")
        faculty = models.Faculty.objects.filter(title = faculty_name).get()
        courses = models.Course.objects.filter(faculty = faculty)
        groups = models.Group.objects.filter(course = course)  
        json_stats = serializers.GroupsByCourse(groups, many=len(groups) > 1).data
        response = {'success': True, 'stats': json_stats}
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
        
    except ObjectDoesNotExist:
        raise Http404()






