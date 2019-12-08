from django.urls import path

from schedule import views


urlpatterns = [
    path('api/groups_list/', views.groups_list),
    path('facultys_list/', views.facultys_list),
    path('list_shedule/',views.list_shedule),
    path('courses_list/', views.courses_list),
    path('groups_by_course/', views.groups_by_course),
    path('api/login', views.login),
]