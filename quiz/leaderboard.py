

def no_of_attempts(quiz, Submission):
    return Submission.objects.filter(quiz=quiz).count()

## returns True, False or None
def is_ans_correct(quiz, student, Submission):
    try:
        sub = Submission.objects.get(student=student, quiz=quiz)
        return sub.answer == quiz.correct_answer
    except Submission.DoesNotExist:
        return None

    if not sub.exists(): return None
    else : return sub[0].answer == quiz.correct_answer

## ---------------------------------------------------------------------

## TODO: override this
from .backend_algorithm import get_final
def get_leaderboard(Quiz, Student, Submission):
    
    array = []
    for quiz in Quiz.objects.all():
        student_subs = []
        for student in Student.objects.all():
            student_subs.append(is_ans_correct(quiz, student, Submission))
        array.append(student_subs)

    return get_final(Student, Quiz, array)

    

    
    
