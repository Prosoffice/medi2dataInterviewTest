from django.urls import path
from .views import LoginView, RegistrationView, LogoutView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
]
