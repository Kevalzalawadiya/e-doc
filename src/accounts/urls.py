from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # path('<str:pagenotfound>/', views.PageNotFound.as_view(), name='pagenot'),
    path('', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('changepass/', views.PasswordChange.as_view(), name='changepass'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('forget-password/', views.ForgetPassword, name="forget_password"),
    path('change-password/<token>/', views.ChangePassword, name="change_password"),
]
