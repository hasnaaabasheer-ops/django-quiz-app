from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .models import Question

@login_required
def quiz(request):
    questions = Question.objects.all()

    score = None
    percentage = None
    result_message = None

    if request.method == "POST":
        score = 0

        for question in questions:
            selected_answer = request.POST.get(
                f"question_{question.id}"
            )

            if selected_answer == question.correct_answer:
                score += 1

        total_questions = questions.count()

        if total_questions > 0:
            percentage = (score / total_questions) * 100

            if percentage >= 80:
                result_message = "Excellent! You did an amazing job! 🏆"
            elif percentage >= 60:
                result_message = "Great job! Keep improving! 🎉"
            elif percentage >= 40:
                result_message = "Good effort! You can do even better! 💪"
            else:
                result_message = "Keep practicing and try again! 📚"

    return render(request, 'quizapp/quiz.html', {
        'questions': questions,
        'score': score,
        'percentage': percentage,
        'result_message': result_message
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()

        return redirect('login')

    return redirect('quiz')