from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import get_object_or_404, render
from .models import Restaurant

def restaurant_status_partial(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurant/_status.html', {'restaurant': restaurant})
