from django.urls import path

from schedule import views


urlpatterns = [
    path('groups_list/', views.groups_list),
]