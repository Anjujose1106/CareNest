from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import FamilyRegisterForm


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