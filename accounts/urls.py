from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('change-avatar/', views.change_avatar, name='change_avatar'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('create-profile/', views.create_profile_view, name='create_profile'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path("change-avatar-htmx/<int:avatar_id>/", views.change_avatar_htmx, name="change_avatar_htmx"),

    # path('restaurant/<int:pk>/status/', views.restaurant_status_partial, name='restaurant-status-partial'),
]
