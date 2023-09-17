from django.urls import path
from . import views

urlpatterns = [

    path('', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('list/', views.AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
]
