from django.contrib.auth.models import User
from django.db.models import F, Q, Sum
from classroom.models import Classroom
from tasks.models import Work
from weekly_test.models import WeeklyTest, AnswerSheet


def student_classroom_points(user:User, classroom:Classroom):
    total_points = 0
    # work of task points
    works = Work.objects.filter( Q(group__members=user) | Q(group=None, submission_by=user), task__classroom=classroom, score__isnull=False)
    work_points = works.aggregate(total_score=Sum('score'))['total_score']
    if work_points != None:
        total_points += work_points
    # tests points
    answersheets = AnswerSheet.objects.filter(user=user, test__weekly__classroom=classroom, submit_time__isnull=False)
    for sheet in answersheets:
        score = sheet.total_score
        if score != None:
            total_points += score
    
    return total_points
    


def student_participation_percetage(user:User, classroom:Classroom):
    classroom_num_task = classroom.all_tasks['num_tasks']
    classroom_num_test = classroom.num_tests
    student_tasks = user.account.group_works(classroom).count() + user.account.indiv_works(classroom).count()
    student_tests = WeeklyTest.objects.filter(weekly__classroom=classroom, 
                                              answersheet__user=user, 
                                              answersheet__submit_time__isnull=False).count()
    num_classroom_activity = classroom_num_task + classroom_num_test
    num_student_activity = student_tasks + student_tests
    if num_classroom_activity == 0:
        return None
    else:
        participation = (num_student_activity/num_classroom_activity)*100
        return participation
    

def student_regularity_points(user:User, classroom:Classroom):
    total_points = 0
    # task regularity  
    group_works = user.account.group_works(classroom)
    indiv_works = user.account.indiv_works(classroom)
    all_works = group_works.union(indiv_works)
    for work in all_works:
        task_deadline_time = work.task.deadline
        submit_time = work.submission_time
        time_elapsed = task_deadline_time - submit_time
        te_seconds = time_elapsed.total_seconds()
        points = te_seconds/1000
        total_points += points
    # test regularity
    answersheets = AnswerSheet.objects.filter(user=user, 
                                              test__weekly__classroom=classroom, 
                                              submit_time__isnull=False).annotate(elapsed_time=F('submit_time') - F('issue_time'))

    for sheet in answersheets:
        time_taken_sec = sheet.elapsed_time.total_seconds()
        points = time_taken_sec / 1000
        total_points += points
    return total_points
            

def get_students_ranking_data(user, classroom:Classroom):
    students = classroom.students.all()
    data_raw = []
    for s in students:
        unit_data = {}
        unit_data['uid'] = s.id
        unit_data['current_user'] = (user==s)
        unit_data['avatar_url'] = s.account.avatar_url
        unit_data['full_name'] = s.account.user_full_name
        unit_data['registration'] = s.account.institutional_id
        unit_data['classroom_points'] = student_classroom_points(s, classroom)
        unit_data['participation'] = student_participation_percetage(s, classroom)
        unit_data['regularity'] = student_regularity_points(s, classroom)
        data_raw.append(unit_data)
    unranked_students = []
    ranked_students = []
    for student_data in data_raw:
        if student_data['classroom_points'] == 0:
            unranked_students.append(student_data)
        else:
            ranked_students.append(student_data)
 
    sorted_ranks = sorted(ranked_students, key=lambda x: (x['classroom_points'], x['participation'], x['regularity']), reverse=True)
    for i, student in enumerate(sorted_ranks):
        student['rank'] = i + 1
    return {'ranked_students':sorted_ranks, 'unranked_students':unranked_students}

    
        
        
        
    
    