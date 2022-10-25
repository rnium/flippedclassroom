from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from classroom.models import Classroom


class Test(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    info = models.CharField(max_length=9999)
    duration_seconds = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    schedule = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Test Id: {self.id}"

    @property
    def total_marks(self):
        questions = self.question_set.all()
        marks = sum([q.marks for q in questions])
        marks_int = int(marks)
        if marks_int == marks:
            return marks_int
        return marks
    
    @property
    def issued_answer_sheets(self):
        answer_sheets = self.answersheet_set.all()
        return answer_sheets
    
    @property
    def submitted_answer_sheets(self):
        answer_sheets = self.answersheet_set.filter(submit_time__isnull=False)
        return answer_sheets
    
    @property 
    def num_answer_sheets(self):
        return self.issued_answer_sheets.count()

    @property 
    def num_submitted_answer_sheets(self):
        return self.submitted_answer_sheets.count()
    
    @property
    def answer_sheet_submitting_users(self):
        users = self.submitted_answer_sheets.values_list("user", flat=True)
        return list(users)



class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    statement = models.CharField(max_length=99999)
    marks = models.FloatField()
    is_descriptive = models.BooleanField(default=False)
    ans_as_img = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Question Id: {self.id} > [{self.test}]"

    @property
    def get_mark(self):
        int_mark = int(self.marks)
        if int_mark == self.marks:
            return int_mark
        return self.marks


class McqOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=9999)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Option Id: {self.id} > [Question Id: {self.question.id}]"


class AnswerSheet(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    test = models.ForeignKey(Test, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_time = models.DateTimeField(blank=True, null=True)
    submit_time = models.DateTimeField(blank=True, null=True)

    @property
    def num_mcq_answers(self):
        return self.mcqanswer_set.count()

    @property
    def num_des_answers(self):
        return self.descriptiveanswer_set.count()

    @property
    def get_score(self):
        if self.num_mcq_answers > 0:
            mcq_score = sum([mcq.score for mcq in self.mcqanswer_set.all()])
            if self.num_des_answers > 0:
                des_score_arr = [des.score for des in self.descriptiveanswer_set.all()]
                try:
                    des_score = sum(des_score_arr)
                    return (mcq_score+des_score)
                except:
                    return 'pending'
            else:
                return mcq_score
        elif self.num_des_answers > 0:
            des_score_arr = [des.score for des in self.descriptiveanswer_set.all()]
            try:
                des_score = sum(des_score_arr)
                return (des_score)
            except:
                return 'pending'
        else:
            return 'empty answer sheet'


class McqAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
    option_chosen = models.ForeignKey(McqOption, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Answer Id: {self.id} to the question {self.question}"
    
    @property
    def score(self):
        if self.option_chosen.is_correct:
            return self.question.get_mark
        else:
            return 0


class DescriptiveAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=9999, null=True)
    answer_img = models.ImageField(upload_to="answers/images/", null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Answer Id: {self.id} to the question {self.question}"
    




