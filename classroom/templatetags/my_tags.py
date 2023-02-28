from django import template

register = template.Library()

@register.filter
def get_score_or_pending(score):
    if score == None:
        return "Pending"
    else:
        return score