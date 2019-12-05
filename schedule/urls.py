from django.urls import path

from schedule import views


urlpatterns = [
    path('groups_list/', views.groups_list),
    path('facultys_list/', views.facultys_list),
    path('list_shedule/',views.list_shedule),
    path('courses_list/', views.courses_list)
]