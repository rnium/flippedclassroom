from django import template
from classroom.models import Classroom
from tasks.models import Task, Work
from weekly_test.models import AnswerSheet

register = template.Library()

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
    qs = Work.objects.filter(user=user, 
                            test__weekly__classroom=classroom, 
                            issue_time__isnull=False, 
                            submit_time__isnull=False)
    qs.order_by('test.created')
    return qs


    