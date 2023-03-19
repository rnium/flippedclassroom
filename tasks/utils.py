import random
from accounts.views import send_html_email
from django.template.loader import render_to_string
from django.urls import reverse
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


def send_newTaskEmailNotif(task, request):
    students = task.classroom.students.all()
    recipant_list = [student.email for student in students]
    url = reverse('classroom:tasks:view_task', args=(task.classroom.id,task.id))
    absolute_uri = request.build_absolute_uri(url)
    email_body = render_to_string('tasks/new_task_notif.html', context={'task':task, 'task_uri':absolute_uri})
    send_html_email(recipant_list, "New task has been assigned", email_body)
    