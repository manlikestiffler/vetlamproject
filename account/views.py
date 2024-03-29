from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import logout

from .forms import *
from .models import UserBase
from .tokens import account_activation_token
from ticket.models import *
from django.db.models import Q
from django.core.mail import send_mail
from vetlamproject.settings import EMAIL_HOST_USER

def staff_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    tickets = Ticket.objects.filter(Q(company__name__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q), ticket_status='Pending')
    context = {'tickets':tickets}
    return render(request, 'home.html', context)

def customer_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else''
    tickets = Ticket.objects.filter(Q(company__name__icontains=q) | Q(title__icontains=q) | Q(description__icontains=q),created_by=request.user)
    context = {'tickets':tickets}
    return render(request, 'home.html', context)    

@login_required
def dashboard(request):
    if request.user.is_staff:
      return staff_view(request)
    else:
        return customer_view(request)

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})
    
@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:login')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('ticket:home')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        data = request.data
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            return redirect('ticket:home')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


# def account_activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = UserBase.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, user.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('account:dashboard')
#     else:
#         return render(request, 'account/registration/activation_invalid.html')

def Logout(request):
    logout(request)
    return redirect('account:login')