from django.urls import path
from . import views

urlpatterns = [
    path('vacancies/', views.get_all_vacancies, name='vacancies'),
    path('vacancies/new/', views.create_vacancy, name='new_vacancy'),
    path('vacancies/applied/', views.get_current_user_applied_vacancies, name='get_current_user_applied_vacancies'),
    path('vacancies/published/', views.get_published_vacancies, name='get_published_vacancies'),
    path('vacancies/<str:id>/', views.get_one_vacancy, name='vacancy'),
    path('vacancies/<str:id>/update/', views.update_vacancy, name='update_vacancy'),
    path('vacancies/<str:id>/delete/', views.delete_vacancy, name='deletete_vacancy'),
    path('vacancies/<str:id>/apply/', views.apply_to_vacancy, name='apply_to_vacancy'),
    path('vacancies/<str:id>/check/', views.is_applied, name='is_applied'),
    path('vacancies/<str:id>/candidates/', views.get_candidates_applied, name='get_candidates_applied'),
]