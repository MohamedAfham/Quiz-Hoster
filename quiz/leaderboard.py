

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
def get_leaderboard(Quiz, Student, Submission):
    lboard = [] ## return [ (student, marks) ]

    for quiz in Quiz.objects.all():
        ## no_of_attempts(quiz, Submission)
        pass

    for student in Student.objects.all():
        ## is_ans_correct(quiz, student, Submission)
        ## marks = calculate_here()
        ## lboard.append( (student, marks) )
        pass


    return lboard
    