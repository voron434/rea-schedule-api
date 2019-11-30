import json


from django.http import JsonResponse, HttpResponse

from schedule import serializers
from schedule import models


def groups_list(request):
    groups = models.Group.objects.all()
    json_stats = serializers.GroupSerializer(groups, many=len(groups) > 1).data
    response = {'success': True, 'stats': json_stats}
    return HttpResponse(json.dumps(response, ensure_ascii=False),
                        content_type="application/json")
    # return JsonResponse(response, safe=False)
