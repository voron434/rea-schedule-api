from django.urls import path

from schedule import views


urlpatterns = [
    path('groups_list/', views.AuthenticatedView.groups_list),
    path('facultys_list/', views.AuthenticatedView.facultys_list),
    path('list_shedule/',views.AuthenticatedView.list_shedule),
    path('courses_list/', views.AuthenticatedView.courses_list),
    path('groups_by_course/', views.AuthenticatedView.groups_by_course),
    path('api/login', views.AuthenticatedView.login),
]