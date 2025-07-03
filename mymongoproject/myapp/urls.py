from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_lead, name='add_lead'),
    path('getall/', views.get_all_leads, name='get_all_leads'),
    path('leads/<str:lead_id>/activities/', views.lead_activity_view, name='lead_activity_view'),
    path('leads/<str:lead_id>/', views.get_lead_by_id, name='get_lead_by_id'),
    path('update/<str:lead_id>/', views.update_lead, name='update_lead'),
    path('delete/<str:lead_id>/', views.delete_lead, name='delete_lead'),
]