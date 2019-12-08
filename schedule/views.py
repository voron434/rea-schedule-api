import json


from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from schedule import serializers
from schedule import models

from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response



class AuthenticatedView(APIView):

    def login(request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=HTTP_200_OK)

    def get_week():
        current_week = datetime.now().isocalendar()[1]
        return current_week

    def groups_list(request):
        groups = models.Group.objects.all()
        json_stats = serializers.GroupSerializer(groups, many=len(groups) > 1).data
        response = {'success': True, 'stats': json_stats}
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
        # return JsonResponse(response, safe=False)

    def facultys_list(request):
        facultys = models.Faculty.objects.all()
        json_stats = serializers.FacultySerializer(facultys, many=len(facultys) > 1).data
        response = {'success': True, 'stats': json_stats}
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

    def list_shedule(request):
        group = request.GET.get("group")
        try:
            group_id = models.Group.objects.values_list('id', flat=True).filter(title = group).get()
            lessons = models.Lesson.objects.filter(group = group_id, week = get_week())
        except ObjectDoesNotExist:
            raise Http404()
        json_stats = serializers.LessonSerializer(lessons, many=len(lessons) > 1).data
        response = {'success': True, 'stats': json_stats}
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

    def courses_list(request):
        faculty_name = request.GET.get("faculty")
        try:
            faculty = models.Faculty.objects.filter(title = faculty_name).get()
            course = models.Course.objects.filter(faculty = faculty)
        except ObjectDoesNotExist:
            raise Http404()
        json_stats = serializers.CourseSerializer(course, many=len(course) > 1).data
        response = {'success': True, 'stats': json_stats}
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

    def groups_by_course(request):
        faculty_name = request.GET.get("faculty")
        course = request.GET.get("course")
        try:
            faculty = models.Faculty.objects.filter(title = faculty_name).get()
            courses = models.Course.objects.filter(faculty = faculty)
            groups = models.Group.objects.filter(course = course)
            json_stats = serializers.GroupsByCourse(groups, many=len(groups) > 1).data
            response = {'success': True, 'stats': json_stats}
            return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
            
        except ObjectDoesNotExist:
            raise Http404()






