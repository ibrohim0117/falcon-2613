from django.shortcuts import render, redirect
from django.views.generic import TemplateView,CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth import login, logout

from apps.mixsins import NotLoginRequiredMixin
from apps.forms import UserLoginForm, UserRegisterForm
from apps.models.user import Users



class UserRegisterView(NotLoginRequiredMixin, CreateView):
    model = Users
    form_class = UserRegisterForm
    template_name = 'auth/register.html'
    success_url = '/'



class UserLoginView(NotLoginRequiredMixin, FormView):
    form_class = UserLoginForm
    template_name = 'auth/login.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        db_user = Users.objects.filter(username=username).first()
        
        if db_user and db_user.check_password(password):
            if db_user.user_type == "operator":
                messages.success(self.request, "Xush kelibsiz ✅")
                login(self.request, db_user)
                return redirect('operator_list')
            else:
                login(self.request, db_user)
                messages.success(self.request, "Xush kelibsiz ✅")
                return redirect(self.success_url)
        
        messages.error(self.request, "Parol yoki Login Xato ❌")
        return self.form_invalid(form)
    


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'

    

def user_logout(request):
    logout(request)
    return redirect('/')


