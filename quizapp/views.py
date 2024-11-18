import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Question

def quiz(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('quiz')  # Redirect to the same page

        marks = []
        for question in Question.objects.all():
            user_ans = request.POST.getlist(f'question_{question.id}')
            user_ans = set(user_ans)
            correct_ans = {opt.text for opt in question.options.filter(is_correct=True)}
            if user_ans == correct_ans:
                marks.append(5)
            else:
                marks.append(-1)
        total_score = sum(marks)
        return render(request, 'quizapp/result.html', {'total_score': total_score})
    else:
        questions = Question.objects.prefetch_related('options').all()
        questions_data = [
            {
                'question': q,
                'options': q.options.all(),
                'is_single_choice': q.options.filter(is_correct=True).count() == 1
            }
            for q in questions
        ]

        # Shuffle questions and their options
        random.shuffle(questions_data)
        for question_data in questions_data:
            question_data['options'] = list(question_data['options'])
            random.shuffle(question_data['options'])
        
        return render(request, 'quizapp/quiz.html', {'questions_data': questions_data})
