from accounts.views import send_html_email
from django.template.loader import render_to_string
from django.urls import reverse


def send_newTestEmailNotif(test, request):
    students = test.weekly.classroom.students.all()
    recipant_list = [student.email for student in students]
    
    email_body = render_to_string('weekly_test/new_test_notif.html', context={'test':test})
    send_html_email(recipant_list, "New test has been announced", email_body)