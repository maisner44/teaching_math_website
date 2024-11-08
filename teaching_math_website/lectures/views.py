from django.shortcuts import render
from .models import Lecture
# Create your views here.


def lectures_list(request):
    lectures = Lecture.objects.all().order_by('-date')
    return render(request, 'lectures/lectures_list.html', {'lectures': lectures})