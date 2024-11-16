from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question
from django.http import HttpResponse
from .forms import AnswerForm

def tests_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/tests_list.html', {'tests': tests})

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()
    if request.method == 'POST':
        form = AnswerForm(request.POST, questions=questions)
        if form.is_valid():
            # Обробка відповідей
            return redirect('tests:tests_list')
    else:
        form = AnswerForm(questions=questions)
    return render(request, 'tests/test_detail.html', {'test': test, 'form': form})

def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    # Тут логіка для обробки результатів тесту
    # Наприклад, збереження результатів, перевірка правильності відповідей

    return HttpResponse("Test submitted successfully!")