from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Enrollment, Submission, Choice


# submit exam
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        selected_choices = request.POST.getlist('choice')

        enrollment = Enrollment.objects.get(
            user=request.user,
            course=course
        )

        submission = Submission.objects.create(
            enrollment=enrollment
        )

        submission.choices.set(selected_choices)
        submission.save()

        return redirect(
            'onlinecourse:show_exam_result',
            course_id=course.id,
            submission_id=submission.id
        )


# show exam result
def show_exam_result(request, course_id, submission_id):

    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    total = 0
    score = 0

    for question in course.question_set.all():
        total += question.grade

        selected_ids = submission.choices.filter(
            question=question
        ).values_list('id', flat=True)

        if question.is_get_score(selected_ids):
            score += question.grade

    grade = round((score / total) * 100, 2)

    context = {
        'course': course,
        'score': score,
        'total': total,
        'grade': grade,
    }

    return render(
        request,
        'onlinecourse/exam_result.html',
        context
    )