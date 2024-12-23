from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/', views.listing, name='listing'),
    path('listing/detail/<int:id>/', views.property_detail, name='property_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('property/create/', views.property_create, name='property_create'),
    path('login/', views.login_view, name='login'),
    path('logout/', CustomLogoutView.as_view(),
         {'next_page': 'home'}, name='logout'),
]
