from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('store:home')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@login_required
def profile(request):
    """User profile view"""
    context = {}
    return render(request, 'accounts/profile.html', context)
