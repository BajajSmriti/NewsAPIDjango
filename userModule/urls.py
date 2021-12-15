from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.HomePageView, name="login"),
    path('register', views.SignUpView, name="register"),
    path('edit_profile', views.EditProfileView, name="edit_profile"),
    path('user_profile/<int:pk>', views.ShowProfilePageView.as_view(), name="user_profile"),
    path('edit_profile_page/<int:pk>', views.EditProfilePageView.as_view(), name="edit_profile_page"),
    path('create_user_profile', views.CreateProfilePageView.as_view(), name="create_user_profile"),
    path('forgotPwd', views.ForgotPwdView, name="forgotPwd"),
]