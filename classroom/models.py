from pathlib import Path
from django.db import models
from django.contrib.auth.models import User
from django.http import FileResponse
from django.templatetags.static import static
import uuid
from os.path import join, basename
from django.utils import timezone
from .utilities import prettify_marks


class Classroom(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    join_code = models.CharField(max_length=10)
    teachers = models.ManyToManyField(User, related_name='teacher')
    students = models.ManyToManyField(User, related_name='student', blank=True)
    banner = models.ImageField(upload_to="classrooms/banner/", null=True, blank=True)
    quote = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.id}"
    
    @property
    def name_max_chars(self):
        return self._meta.get_field('name').max_length
    
    @property
    def course_max_chars(self):
        return self._meta.get_field('course').max_length
    
    @property
    def quote_max_chars(self):
        return self._meta.get_field('quote').max_length
    
    @property
    def banner_url(self):
        if bool(self.banner):
            return self.banner.url
        else:
            return static('classroom/images/default_bg.svg')
    
    @property
    def num_students(self):
        return self.students.count()
    
    @property
    def teacher_name(self):
        teachers = self.teachers.all()
        if len(teachers) > 0:
            teacher1 = teachers[0]
            first_name = teacher1.first_name
            if first_name:
                return first_name
            else:
                return teacher1.username
        else:
            return None

    @property
    def active_status_css_class(self):
        if self.active:
            return "online"
        else:
            return "offline"
    
    @property
    def last_post_time(self):
        if self.classroompost_set.count() > 0:
            post = self.classroompost_set.latest('posted')
            return post.posted
        else:
            return False

    @property
    def upcoming_tests(self):
        test_qs = [w.all_upcoming_tests for w in self.weeklies]
        if len(test_qs) > 1:
            t_qs_0 = test_qs[0]
            t_qs_others = test_qs[1:]
            final_qs = t_qs_0.union(*t_qs_others)
            return final_qs.order_by("schedule")
        elif len(test_qs) == 1:
            return test_qs[0].order_by("schedule")
        else:
            return self.weekly_set.none()
        
    @property
    def previous_tests(self):
        test_qs = [w.all_prev_tests for w in self.weeklies]
        if len(test_qs) > 1:
            t_qs_0 = test_qs[0]
            t_qs_others = test_qs[1:]
            final_qs = t_qs_0.union(*t_qs_others)
            return final_qs.order_by("schedule")
        elif len(test_qs) == 1:
            return test_qs[0].order_by("schedule")
        else:
            return self.weekly_set.none()
    
    @property
    def non_live_tests(self):
        up_tests = self.upcoming_tests
        prev_tests = self.previous_tests
        num_tests = len(up_tests) + len(prev_tests)
        has_nl_tests = bool(num_tests)
        return {'has_nl_tests':has_nl_tests, 'num_tests':num_tests, 'up_tests':up_tests, 'prev_tests':prev_tests}
    
    @property
    def ongoing_tests(self):
        test_qs = [w.ongoing_test for w in self.weeklies]
        if len(test_qs) > 1:
            t_qs_0 = test_qs[0]
            t_qs_others = test_qs[1:]
            final_qs = t_qs_0.union(*t_qs_others)
            return final_qs.order_by("schedule")
        elif len(test_qs) == 1:
            return test_qs[0].order_by("schedule")
        else:
            return self.weekly_set.none()
    
    def students_non_participating_ongoing_tests(self, student):
       test_qs = [w.ongoing_test.exclude(answersheet__user=student) for w in self.weeklies]
       if len(test_qs) > 1:
           t_qs_0 = test_qs[0]
           t_qs_others = test_qs[1:]
           final_qs = t_qs_0.union(*t_qs_others)
           return final_qs.order_by("expiration")
       elif len(test_qs) == 1:
           return test_qs[0].order_by("expiration")
       else:
           return self.weekly_set.none()

    @property
    def weeklies(self):
        qs = self.weekly_set.all().order_by('created')
        return qs
    
    @property
    def num_weeklies(self):
        return self.weeklies.count()
    
    @property
    def has_weeklies(self):
        return bool(self.num_weeklies)
    
    @property
    def num_posts(self):
        return self.classroompost_set.count()
    
    @property
    def assigned_tasks(self):
        return self.task_set.all()
    
    @property
    def current_tasks(self):
        timenow = timezone.now()
        qs = self.assigned_tasks.filter(deadline__gte=timenow).order_by("deadline")
        return qs

    @property
    def prev_tasks(self):
        timenow = timezone.now()
        qs = self.assigned_tasks.filter(deadline__lt=timenow).order_by("deadline")
        return qs
    
    @property
    def all_tasks(self):
        ongoing_task = self.current_tasks
        prev_task = self.prev_tasks
        num_tasks = len(ongoing_task) + len(prev_task)
        has_tasks = bool(num_tasks)
        return {'has_tasks':has_tasks, 'num_tasks':num_tasks, 'ongoing_task':ongoing_task, 'prev_task':prev_task}
    
    @property
    def assigned_group_tasks_list(self):
        tasks = self.assigned_tasks
        return [task for task in tasks if task.is_group_task]
    
    @property
    def assigned_indiv_tasks_list(self):
        tasks = self.assigned_tasks
        return [task for task in tasks if not task.is_group_task]
    
    @property
    def num_tasks(self):
        return self.assigned_tasks.count()
    
    @property 
    def num_group_tasks(self):
        return len(self.assigned_group_tasks_list)
        
    @property 
    def num_indiv_tasks(self):
        return len(self.assigned_indiv_tasks_list)
    
    @property
    def assigned_tasks_total_marks(self):
        tasks = self.assigned_tasks
        marks = tasks.aggregate(models.Sum('marks'))['column__sum']
        return marks
    
    @property
    def group_tasks_total_marks(self):
        tasks = self.assigned_group_tasks_list
        marks = sum([task.marks for task in tasks])
        return prettify_marks(marks)
    
    @property
    def indiv_tasks_total_marks(self):
        tasks = self.assigned_indiv_tasks_list
        marks = sum([task.marks for task in tasks])
        return marks
    
    @property
    def pre_class_total_marks(self):
        weeklies = self.weeklies
        total_marks = 0
        for weekly in weeklies:
            total_marks += weekly.pre_cls_marks
        return total_marks
    
    @property
    def in_class_total_marks(self):
        weeklies = self.weeklies
        total_marks = 0
        for weekly in weeklies:
            total_marks += weekly.in_cls_marks
        return total_marks
    
    @property
    def post_class_total_marks(self):
        weeklies = self.weeklies
        total_marks = 0
        for weekly in weeklies:
            total_marks += weekly.post_cls_marks
        return total_marks
    
    @property
    def num_tests(self):
        weeklies = self.weekly_set.all()
        count = sum([w.num_tests for w in weeklies])
        return count
    
    @property
    def classroom_tests_total_marks(self):
        weeklies = self.weekly_set.all()
        all_tests_marks = sum([weekly.tests_total_marks for weekly in weeklies])
        return all_tests_marks
            

class PostTopic(models.Model):
    name = models.CharField(max_length=100)
    str_id = models.CharField(max_length=100)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    @property
    def num_posts(self):
        return self.classroompost_set.count()
    
    @property
    def has_posts(self):
        return bool(self.num_posts)
    
    @property
    def posts(self):
        return self.classroompost_set.order_by('-posted')


class ClassroomPost(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    description = models.CharField(max_length=9999)
    topics = models.ManyToManyField(PostTopic)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post id-{self.id} of: {self.classroom}"
    
    @property
    def num_comments(self):
        return self.comment_set.count()

    @property
    def num_attachments(self):
        return self.postattachment_set.count()

    @property
    def has_comments(self):
        if self.num_comments > 0:
            return True
        else:
            return False
    
    @property
    def has_topics(self):
        if self.topics.count() > 0:
            return True
        else:
            return False
    

    @property
    def has_attachments(self):
        if self.num_attachments > 0:
            return True
        else:
            return False   


class PostAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.classroom_post.classroom.id), filename)

    classroom_post = models.ForeignKey(ClassroomPost, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath)

    @property
    def filename(self):
        return str(basename(self.attached_file.name))
    
    @property
    def css_class(self):
        css_classes = {
            ".pdf": "bx bxs-file-pdf",
            ".pptx":"bx bx-slideshow",
            ".jpg": "bx bxs-file-image",
            ".png": "bx bxs-file-image",
            ".docx": "bx bxs-file-doc",
            ".zip": "bx bxs-file-archive",
            ".txt": "bx bxs-file-txt",
            ".py": "bx bxl-python",
            ".pyw": "bx bxl-python"
        }
        file_extention = Path(self.filename).suffix
        if file_extention in css_classes:
            return css_classes[file_extention]
        else:
            return "bx bxs-file-blank"

    
class Comment(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    post = models.ForeignKey(ClassroomPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply')
    comment_text = models.CharField(max_length=9999)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment object({self.id}) of post:<{self.post.id}>"

    @property
    def is_thread(self):
        # a thread is a type of comment which has no parent comment (not a reply comment)
        if self.parent is None:
            return True
        else:
            return False

    @property
    def has_replies(self):
        num_replies = self.reply.count()
        if num_replies > 0:
            return True
        else:
            return False
    
    @property
    def cssClass(self):
        if self.author in self.post.classroom.teachers.all():
            # user-teacher class has a teacher badge in it
            return "username user-teacher"
        else:
            return "username"
    
    @property
    def replies(self):
        return self.reply.all().order_by("comment_time")


class Assignment(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    instructions = models.TextField(null=True, blank=True)
    submission_deadline = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)


class AssignmentAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments/assignments", str(self.assignment.classroom.id), filename)

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath)

    @property
    def filename(self):
        return str(basename(self.attached_file.name))
    
    
class AssessmentMeta(models.Model):
    classroom = models.OneToOneField(Classroom, on_delete=models.CASCADE)
    attendance_marks = models.FloatField(default=10)
    classtest_marks = models.FloatField(default=15)
    pre_class_marks = models.FloatField(default=5)
    in_class_marks = models.FloatField(default=5)
    post_class_marks = models.FloatField(default=5)
    
    def __str__(self):
        return f"{self.classroom.id} - Assessment meta"
    
    @property
    def assessments(self):
        return self.assessment_set.all().order_by('student__account__institutional_id')
    
    @property
    def total_marks(self):
        marks = (self.attendance_marks + self.classtest_marks + self.pre_class_marks 
                + self.in_class_marks + self.post_class_marks)
        return prettify_marks(marks)
    
    @property
    def get_attendance_marks(self):
        return prettify_marks(self.attendance_marks)
    
    @property
    def get_classtest_marks(self):
        return prettify_marks(self.classtest_marks)
    
    @property
    def get_preclass_marks(self):
        return prettify_marks(self.pre_class_marks)
    
    @property
    def get_inclass_marks(self):
        return prettify_marks(self.in_class_marks)
    
    @property
    def get_postclass_marks(self):
        return prettify_marks(self.post_class_marks)
    
    # @property
    # def get_indiv_task_marks(self):
    #     return prettify_marks(self.indiv_task_marks)
    
    @property
    def num_weekly_tests(self):
        return sum([w.num_tests for w in self.weekly_set.all()])
    
    # @property
    # def get_weekly_test_marks(self):
    #     return prettify_marks(self.weekly_test_marks)
 
    
class Assessment(models.Model):
    meta = models.ForeignKey(AssessmentMeta, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance_score = models.FloatField(null=True, blank=True)
    classtest_score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"User-{self.student.id} assessment of classroom {self.meta.classroom.id}"
    
    @property
    def get_attendance_score(self):
        return prettify_marks(self.attendance_score)
    
    @property
    def get_classtest_score(self):
        return prettify_marks(self.classtest_score)
    
    @property
    def group_task_points(self):
        points = self.student.account.group_task_total_points(self.meta.classroom)
        return prettify_marks(points)
    
    @property
    def group_task_score(self):
        students_gw_total_score = self.student.account.group_task_total_points(self.meta.classroom)
        if students_gw_total_score == None:
            return None
        group_tasks_total_marks = self.meta.classroom.group_tasks_total_marks
        if group_tasks_total_marks <= 0:
            return 0
        score_per_mark = students_gw_total_score/group_tasks_total_marks
        obtained_score = score_per_mark*self.meta.group_task_marks
        return prettify_marks(obtained_score)
   
    # \\ sections total score
    @property
    def pre_cls_points(self):
        points = self.student.account.pre_class_points(self.meta.classroom)
        return points
    
    @property
    def pre_cls_marks(self):
        return self.meta.classroom.pre_class_total_marks
        
    @property
    def pre_class_score(self):
        students_preclass_total_score = self.pre_cls_points
        if students_preclass_total_score == None:
            return None
        precls_total_marks = self.pre_cls_marks
        if precls_total_marks <= 0:
            return 0
        score_per_mark = students_preclass_total_score/precls_total_marks
        obtained_score = score_per_mark*self.meta.pre_class_marks
        return prettify_marks(obtained_score)
    
    
    @property
    def in_cls_points(self):
        points = self.student.account.in_class_points(self.meta.classroom)
        return points
    
    @property
    def in_cls_marks(self):
        return self.meta.classroom.in_class_total_marks
    
    
    @property
    def in_class_score(self):
        students_inclass_total_score = self.student.account.in_class_points(self.meta.classroom)
        if students_inclass_total_score == None:
            return None
        incls_total_marks = self.meta.classroom.in_class_total_marks
        if incls_total_marks <= 0:
            return 0
        score_per_mark = students_inclass_total_score/incls_total_marks
        obtained_score = score_per_mark*self.meta.in_class_marks
        return prettify_marks(obtained_score)
    
    
    @property
    def post_cls_points(self):
        points = self.student.account.post_class_points(self.meta.classroom)
        return points
    
    @property
    def post_cls_marks(self):
        return self.meta.classroom.post_class_total_marks
    
    
    @property
    def post_class_score(self):
        students_total_score = self.student.account.post_class_points(self.meta.classroom)
        if students_total_score == None:
            return None
        total_marks = self.meta.classroom.post_class_total_marks
        if total_marks <= 0:
            return 0
        score_per_mark = students_total_score/total_marks
        obtained_score = score_per_mark*self.meta.post_class_marks
        return prettify_marks(obtained_score)
    # //
    @property
    def indiv_task_points(self):
        points = self.student.account.indiv_task_total_points(self.meta.classroom)
        return prettify_marks(points)
    
    @property
    def indiv_task_score(self):
        students_iw_total_score = self.student.account.indiv_task_total_points(self.meta.classroom)
        if students_iw_total_score == None:
            return None
        indiv_tasks_total_marks = self.meta.classroom.indiv_tasks_total_marks
        if indiv_tasks_total_marks <= 0:
            return 0
        score_per_mark = students_iw_total_score/indiv_tasks_total_marks
        obtained_score = score_per_mark*self.meta.indiv_task_marks
        return prettify_marks(obtained_score)
        
    @property
    def weekly_tests_points(self):
        points = self.student.account.classroom_test_points(self.meta.classroom)
        return prettify_marks(points)
        
    @property
    def weekly_tests_score(self):
        students_points = self.student.account.classroom_test_points(self.meta.classroom)
        if students_points == None:
            return None
        classroom_tests_total_marks = self.meta.classroom.classroom_tests_total_marks
        if classroom_tests_total_marks <= 0:
            return 0
        score_per_mark = students_points/classroom_tests_total_marks
        obtained_score = score_per_mark*self.meta.weekly_test_marks
        return prettify_marks(obtained_score)
    
    @property
    def total_score(self):
        scores = [
            self.attendance_score,
            self.classtest_score,
            self.pre_class_score,
            self.in_class_score,
            self.post_class_score
        ]
        if all([score!=None for score in scores]):
            total = sum(scores)
            return prettify_marks(total)
        else:
            return None
    
    @property
    def num_group_work(self):
        return self.student.account.group_works(self.meta.classroom).count()
    
    @property
    def num_indiv_works(self):
        return self.student.account.indiv_works(self.meta.classroom).count()
    
    @property
    def num_participated_tests(self):
        return self.student.account.classroom_test_answersheets(self.meta.classroom).count()
    
    @property
    def score_percentage(self):
        total_score = self.total_score
        total_marks = self.meta.total_marks
        if total_marks==None or total_score==None:
            return None
        if total_marks <= 0:
            return 0
        score_per_mark = total_score/total_marks
        percentage_score = score_per_mark * 100
        return prettify_marks(percentage_score)
    
    
class Congratulation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    added = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)