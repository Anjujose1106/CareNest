from django.shortcuts import render, get_object_or_404
from .models import Carer


def carer_list(request):
    carers = Carer.objects.all()

    return render(
        request,
        'carers/carer_list.html',
        {'carers': carers}
    )
def home(request):
    return render(
        request,
        'carers/home.html'
    )


def carer_detail(request, id):
    carer = get_object_or_404(
        Carer,
        id=id
    )

    return render(
        request,
        'carers/carer_detail.html',
        {'carer': carer}
    )
def join(request):
    return render(
        request,
        'carers/join.html'
    )