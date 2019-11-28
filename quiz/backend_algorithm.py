# res_list: 2D array of values 0 and 1, 0 if the answer is wrong 1 if the answer,
# is correct, "Did Not Attempt" if not attempted. 

def get_avg(qID,res_list):
    correct_answers = res_list[qID].count(True)
    total_questions = len(res_list[qID])
    return (correct_answers/total_questions)

def score(avg,qID,teamID, res_list):
    result = res_list[qID][teamID]
    if result == True:
        q_score = 3 + 7*(1-avg)**2
    else:
        q_score = 0
    return q_score

def update_score(teamID,qID,res_list, team_score):
    team_score[teamID] = team_score[teamID] + round(score(get_avg(qID,res_list),qID,teamID,res_list),1)
    return team_score

def get_final(Student, Quiz, res_list):
    team_score = [0]*Student.objects.count()
    for qID in range(Quiz.objects.count()):

        for teamID in range(Student.objects.count()):
            team_scores = update_score(teamID,qID, res_list, team_score)

    ret = [] ## 
    for i in range(Student.objects.count()):
        ret.append([Student.objects.all()[i],team_scores[i]])
    return ret








     
