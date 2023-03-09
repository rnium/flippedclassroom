from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import F, Q, Sum
from classroom.models import Classroom
from tasks.models import Work
from weekly_test.models import WeeklyTest, AnswerSheet
import jwt


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
        try:
            time_elapsed = task_deadline_time - submit_time
        except TypeError:
            continue
        te_seconds = time_elapsed.total_seconds()
        points = te_seconds/1000
        total_points += points
    # test regularity
    answersheets = AnswerSheet.objects.filter(user=user, 
                                              test__weekly__classroom=classroom, 
                                              submit_time__isnull=False).annotate(elapsed_time=F('submit_time') - F('issue_time'))

    for sheet in answersheets:
        test_duration = sheet.test.duration_seconds
        time_taken_sec = sheet.elapsed_time.total_seconds()
        points = (test_duration-time_taken_sec) / 100
        total_points += points
    return total_points


def scale_to_percent(datalist:list):
    # Scale values to range 0-100
    if len(datalist) == 0:
        return 0
    min_val = min(datalist)
    max_val = max(datalist)
    scaled_values = [] 
    for val in datalist:
        numerator = val - min_val
        denom = max_val - min_val
        if denom == 0:
            return 0
        else:
            scaled = (numerator/denom) * 100
            scaled_values.append(scaled)
    return scaled_values
       

def get_students_ranking_data(classroom:Classroom, user=None):
    students = classroom.students.all()
    data_raw = []
    for s in students:
        unit_data = {}
        unit_data['uid'] = s.id
        if user != None:
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
    toppers_list = sorted_ranks[0:3]
    toppers_data = {}
    for topper in toppers_list:
        # generating jwt for proper ranking congratulation
        jwt_payload = {'uid':topper['uid'], 'rank':topper['rank']}
        topper_jwt = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm='HS256')
        topper['jwt'] = topper_jwt
        if topper['rank'] == 1:
            toppers_data['first'] = topper
        elif topper['rank'] == 2:
            toppers_data['second'] = topper
        elif topper['rank'] == 3:
            toppers_data['third'] = topper
        
        
    return {'ranked_students':sorted_ranks, 'toppers':toppers_data, 'unranked_students':unranked_students}


def get_students_stats_data(classroom):
    students = classroom.students.all()
    data_raw = []
    for s in students:
        unit_data = {}
        unit_data['full_name'] = s.account.user_full_name
        unit_data['registration'] = s.account.institutional_id
        unit_data['points'] = student_classroom_points(s, classroom)
        unit_data['participation'] = student_participation_percetage(s, classroom)
        unit_data['regularity'] = student_regularity_points(s, classroom)
        data_raw.append(unit_data)
    sorted_students = sorted(data_raw, key=lambda x: (x['registration']), reverse=False)
    return sorted_students
    

def get_students_performance_chart_data(classroom:Classroom):
    """_summary_
    output format will be;
    {
        "data": {
            'points': {
                'raw': ['data', 'data'],
                'scaled': ['data', 'data'],
            },
            'regularity': {
                'raw': ['data', 'data'],
                'scaled': ['data', 'data'],
            }
            'studentNames': []
            'participation': []
        }
    }
    """
    data = {
        'points': {},
        'regularity':{},
    }
    data['has_stats'] = True
    student_stats_data = get_students_stats_data(classroom)
    raw_points = [student['points'] for student in student_stats_data]
    if not any(raw_points):
        data['has_stats'] = False
        return data
    data['studentNames'] = [student['full_name'] for student in student_stats_data]
    scaled_points = scale_to_percent(raw_points)
    data['points'] = {'raw':raw_points, 'scaled':scaled_points}
    data['participation'] = [student['participation'] if student['participation'] != None else 0  for student in student_stats_data]
    raw_regularity = [student['regularity'] for student in student_stats_data]
    scaled_regularity = scale_to_percent(raw_regularity)
    data['regularity'] = {'raw':raw_regularity, 'scaled':scaled_regularity}

    return data
    
    
    
    
        
        
        
    
    