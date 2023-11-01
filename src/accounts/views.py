from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .models import *
from .forms import UserRegistration, LoginFormAuthentication, PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.db.models import Q
from .helper import send_forget_password_mail
from django.contrib import messages
import uuid
from django.urls import reverse_lazy



class UserRegister(CreateView):
    template_name = "accounts/register-user.html"
    form_class = UserRegistration
    success_url = "/"


class UserLoginView(LoginView):
    form_class = LoginFormAuthentication
    template_name = "accounts/login-user.html"
    success_url = reverse_lazy('document:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.success_url)


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "accounts/change-passwords.html"
    success_url = "/profile/"


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class UserLogout(LogoutView):
    template_name = "accounts/login-user.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect("login")



# class PageNotFound(TemplateView):
# Todo: override defualt page not found
#     template_name = 'accounts/page-error-404.html'


def custom_404_error(request, exception):
    return render(request, "accounts/page-error-404.html", status=404)


def ChangePassword(request, token):
    context = {}
    try:
        user = AdminUser.objects.get(forget_password_token=token)
        context = {"user_id": user.id}

        if request.method == "POST":
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("reconfirm_password")
            user_id = request.POST.get("user_id")

            if user_id is None:
                print('this is called ')
                messages.success(request, "No user id found.")
                return redirect(f"/accounts/change-password/{token}/")

            if new_password != confirm_password:
                print('this is not called.')
                messages.success(request, "Passwords do not match.")
                return redirect(f"/accounts/change-password/{token}/")

            user.set_password(new_password)
            user.forget_password_token = None
            user.save()
            
            return redirect("login")

    except Exception as e:
        print(e)
    return render(request, "/accounts/change-password.html", context)


def ForgetPassword(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            user_obj = AdminUser.objects.filter(
                Q(email=username) | Q(username=username)
            ).first()
            print(True)
            if not user_obj:
                messages.error(request, "No user found with this username or email.")
                return redirect("forget_password")

            token = str(uuid.uuid4())
            user_obj.forget_password_token = token
            user_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, "An email has been sent.")
            return redirect("forget_password")
    except Exception as e:
        print(e)
    return render(request, "accounts/forget-password.html")
