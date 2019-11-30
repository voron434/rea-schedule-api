from django.shortcuts import render

from django.http import JsonResponse

from schedule import serializers
from schedule import models
# Create your views here.


def groups_list(request):
    groups = models.Group.objects.all()
    json_stats = serializers.GroupSerializer(groups, many=len(groups) > 1).data
    response = {'success': True, 'stats': json_stats}
    print(response)
    return JsonResponse(response)