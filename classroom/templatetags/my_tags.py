from django import template
from django.db.models import Q
from classroom.models import Classroom
from tasks.models import Task, Work
from weekly_test.models import WeeklyTest, AnswerSheet

register = template.Library()

@register.filter
def prettify_marks(marks_raw):
    if marks_raw == None:
        return None
    marks_int = int(marks_raw)
    if marks_int != marks_raw:
        return round(marks_raw, 2)
    else:
        return marks_int
    
@register.filter
def get_score_or_pending(score):
    if score == None:
        return "Pending"
    else:
        return score


@register.filter
def get_score_or_asterisk(score):
    if score == None:
        return "**"
    else:
        return score
    
@register.filter
def get_total_score_css_class(score):
    if score == None:
        return "pending"
    else:
        return ""
    
@register.simple_tag
def get_test_participations(user, classroom):
    qs = AnswerSheet.objects.filter(user=user, 
                                    test__weekly__classroom=classroom, 
                                    issue_time__isnull=False, 
                                    submit_time__isnull=False)
    qs.order_by('test.created')
    return qs    

@register.simple_tag
def get_task_participations(user, classroom):
    qs = Work.objects.filter( Q(group__members=user) | Q(group=None, submission_by=user), task__classroom=classroom)
    qs.order_by('task.addded')
    return qs

# homepage: data for teachers
@register.simple_tag
def get_unchecked_tests(classroom):
    tests_qs = WeeklyTest.objects.filter(weekly__classroom=classroom).order_by("created")
    pending_tests = []
    for test in tests_qs:
        answersheets = test.submitted_answer_sheets
        sheet_scores = [sheet.total_score for sheet in answersheets]
        pending_scores = [score for score in sheet_scores if score is None]
        num_pending_scores = len(pending_scores)
        if num_pending_scores == 0:
            continue
        test.total_sheets = answersheets.count()
        test.pending_sheets = num_pending_scores
        pending_tests.append(test)
    
    return pending_tests
            
@register.simple_tag
def get_unchecked_tasks(classroom):
    tasks_qs = Task.objects.filter(classroom=classroom).order_by("addded")
    pending_tasks = []
    for task in tasks_qs:
        works = Work.objects.filter(is_submitted=True, task=task)
        
        work_scores = [work.score for work in works]
        pending_scores = [score for score in work_scores if score is None]
        num_pending_scores = len(pending_scores)
        if num_pending_scores == 0:
            continue
        task.total_works = works.count()
        task.pending_works = num_pending_scores
        pending_tasks.append(task)
    
    return pending_tasks
            
        
        
    
    
    