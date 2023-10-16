from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

  path('get_specialies/', views.get_specialies),

  
  path('register/', views.register),
  path('login/', views.login),


  path('get_user_profile/', views.get_user_profile),
  path('edit_profile/', views.edit_profile),


  path('get_teacher_profile/', views.get_teacher_profile),


  path('create_course/', views.create_course),
  path('get_teacher_courses/', views.get_teacher_courses),
  path('edit_teacher_course/', views.edit_teacher_course),
  path('delete_course/', views.delete_course),


  path('get_all_courses/', views.get_all_courses),



  path('add_to_fav/', views.add_to_fav),
  path('get_student_fav/', views.get_student_fav),
  path('delete_from_fav/', views.delete_from_fav),
  path('delete_all_fav/', views.delete_all_fav),



  path('create_course_review/', views.create_course_review),
  path('update_course_review/', views.update_course_review),
  path('get_course_review/', views.get_course_review),




  path('get_enrollments/', views.get_enrollments),





]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



