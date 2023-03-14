import random
from accounts.views import send_html_email
from celery import shared_task
from django.template.loader import render_to_string

def random_subsets(lst, num_item):
    random.shuffle(lst)
    subsets_container = []
    while bool(len(lst)):
        if len(lst) >= num_item:
            subset = [lst.pop() for i in range(num_item)]
            subsets_container.append(subset)
        elif len(lst) >= 1:
            subsets_container.append(lst)
            break
        else:
            break
    return subsets_container


# @shared_task
def send_newTaskEmailNotif(task):
    students = task.classroom.students.all()
    recipant_list = [student.email for student in students]
    email_body = render_to_string('tasks/new_task_notif.html')
    send_html_email(recipant_list, "New task has been assigned", email_body)
    