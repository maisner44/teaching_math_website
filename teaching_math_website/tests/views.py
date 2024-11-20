from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, TestResult, AnswerSelection, Answer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
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
            # Тут ми повинні зібрати відповіді користувача та перевірити їх
            user_answers = []
            correct_answers = 0
            
            for question in questions:
                # Отримуємо відповідь користувача
                answer_id = form.cleaned_data.get(f'question_{question.id}')
                user_answers.append(answer_id)

                # Перевіряємо, чи правильна відповідь
                correct_answer = question.correct_answer.id
                if int(answer_id) == correct_answer:
                    correct_answers += 1
           
            # Зберігаємо результат тесту для користувача
            print(correct_answers,'----------------')
            test = get_object_or_404(Test, id=test_id)
            if TestResult.objects.filter(user=request.user, test=test).first():
                return redirect('tests:already_pass', test_id=test.id)
            
            result = TestResult.objects.create(
                user=request.user,
                test=test,
                score=str(correct_answers),
                total_questions=questions.count(),
            )
            print(result.score, result.total_questions,'-------------')

            # Перенаправляємо на сторінку результатів тесту
            return redirect('tests:test_results', test_id=test.id)

    else:
        form = AnswerForm(questions=questions)

    return render(request, 'tests/test_detail.html', {'test': test, 'form': form})

def test_results(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    # Отримуємо результат тесту для цього користувача
    result = TestResult.objects.filter(user=request.user, test=test).last()
    result.refresh_from_db()

    if result:
        # Відображаємо результат тесту
        return render(request, 'tests/test_results.html', {'result': result, 'test': test})
    else:
        # Якщо результатів ще немає (наприклад, користувач не здав тест)
        return HttpResponse("You have not completed this test yet.")

def already_pass(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    result = TestResult.objects.filter(user=request.user, test=test).last()
    result.refresh_from_db()
    if result:
        # Відображаємо результат тесту
        return render(request, 'tests/test_results_already_pass.html', {'result': result, 'test': test})
    else:
        # Якщо результатів ще немає (наприклад, користувач не здав тест)
        return HttpResponse("You have not completed this test yet.")

def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    # Your logic for submitting the test goes here.
    # For example, you could handle form submissions or process test answers.
    
    # return render(request, 'tests/submit_test.html', {'test': test})