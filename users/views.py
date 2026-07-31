from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import FamilyRegisterForm
from django.contrib.auth.decorators import login_required

def register(request):

    if request.method == 'POST':

        form = FamilyRegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('/')

    else:

        form = FamilyRegisterForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )


def custom_logout(request):

    logout(request)

    return redirect('/')




@login_required
def dashboard_redirect(request):
    
    if request.user.is_superuser:        
        return redirect('/admin-dashboard/')

    if hasattr(request.user, 'carer_profile'):
        return redirect('/carer-dashboard/')

    return redirect('/')