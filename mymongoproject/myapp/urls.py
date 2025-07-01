from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_lead, name='add_lead'),
    path('getall/', views.get_all_leads, name='get_all_leads'),
    path('update/<str:lead_id>/', views.update_lead, name='update_lead'),
    path('delete/<str:lead_id>/', views.delete_lead, name='delete_lead'),
]