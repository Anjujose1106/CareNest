from django.shortcuts import render, get_object_or_404, redirect
from .models import Carer
from .forms import CarerApplicationForm

def carer_list(request):

    carers = Carer.objects.all()

    postcode = request.GET.get('q')
    care_type = request.GET.get('care_type')

    if postcode:
        carers = carers.filter(
            postcode__icontains=postcode
        )

    if care_type:
        carers = carers.filter(
            care_type=care_type
        )

    return render(
        request,
        'carers/carer_list.html',
        {
            'carers': carers
        }
    )
def home(request):
    return render(
        request,
        'carers/home.html'
    )


from reviews.models import Review

def carer_detail(request, id):
    carer = get_object_or_404(Carer, id=id)

    reviews = Review.objects.filter(
        carer=carer
    )

    return render(
        request,
        'carers/carer_detail.html',
        {
            'carer': carer,
            'reviews': reviews,
        }
    )
def join(request):
    return render(
        request,
        'carers/join.html'
    )
def apply_carer(request):

    if request.method == 'POST':

        form = CarerApplicationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/join/success/')

    else:
        form = CarerApplicationForm()

    return render(
        request,
        'carers/apply_carer.html',
        {'form': form}
    )
def join_success(request):
    return render(
        request,
        'carers/join_success.html'
    )