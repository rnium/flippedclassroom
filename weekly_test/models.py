from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
from weeklies.models import Weekly


class WeeklyTest(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    info = models.CharField(max_length=9999)
    preclass = models.BooleanField(default=False)
    inclass = models.BooleanField(default=False)
    postclass = models.BooleanField(default=False)
    duration_seconds = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    schedule = models.DateTimeField()
    expiration = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

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
    def num_questions(self):
        return self.question_set.count()
    
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
        
    @property
    def weekly_section(self):
        if self.preclass:
            return "PreClass"
        elif self.inclass:
            return "InClass"
        elif self.postclass:
            return "PostClass"
        else:
            return "Weekly General"


class Question(models.Model):
    test = models.ForeignKey(WeeklyTest, on_delete=models.CASCADE)
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
    test = models.ForeignKey(WeeklyTest, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_test_user')
    issue_time = models.DateTimeField(blank=True, null=True)
    submit_time = models.DateTimeField(blank=True, null=True)

    @property
    def num_mcq_answers(self):
        return self.mcqanswer_set.count()

    @property
    def num_des_answers(self):
        return self.descriptiveanswer_set.count()

    @property
    def total_score(self):
        if self.num_mcq_answers > 0:
            mcq_score = sum([mcq.score for mcq in self.mcqanswer_set.all()])
            if self.num_des_answers > 0:
                des_score_arr = [des.score for des in self.descriptiveanswer_set.all()]
                try:
                    des_score = sum(des_score_arr)
                    return (mcq_score+des_score)
                except:
                    return None
            else:
                return mcq_score
        elif self.num_des_answers > 0:
            des_score_arr = [des.score for des in self.descriptiveanswer_set.all()]
            try:
                des_score = sum(des_score_arr)
                return (des_score)
            except:
                return None
        else:
            return 0
    
    @property
    def get_score(self):
        raw_score = self.total_score
        int_score = int(raw_score)
        if int_score == raw_score:
            return int_score
        else:
            return raw_score
    
    @property
    def num_correct_ans(self):
        mcq_corrects = self.mcqanswer_set.filter(option_chosen__is_correct=True).count()
        des_corrects = self.descriptiveanswer_set.filter(score__isnull=False).filter(score__gt=0).count()
        return mcq_corrects + des_corrects
    
    @property
    def answers(self):
        des_answers = self.descriptiveanswer_set.all()
        mcq_answers = self.mcqanswer_set.all()
        return {'des_answers':des_answers, 'mcq_answers':mcq_answers}


class McqAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
    option_chosen = models.ForeignKey(McqOption, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Answer Id: {self.id} to the question {self.question}"
    
    @property
    def is_correct_ans(self):
        if self.option_chosen.is_correct:
            return True
        else:
            return False
        
    
    @property
    def score(self):
        if self.is_correct_ans:
            return self.question.get_mark
        else:
            return 0
    
    @property
    def options_data(self):
        options = self.question.mcqoption_set.all()
        returning_dataset = []
        choice_code = ord("A")
        for option in options:
            unit_data = {}
            unit_data['choice_code'] = chr(choice_code)
            choice_code += 1
            unit_data['option_text'] = option.option_text
            if option.is_correct:
                unit_data['css_class'] = 'correct'
            else:
                if option == self.option_chosen:
                    unit_data['css_class'] = 'incorrect'
                else:
                    unit_data['css_class'] = ''
            returning_dataset.append(unit_data)
        return returning_dataset
            
            


class DescriptiveAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=9999, null=True)
    answer_img = models.ImageField(upload_to="answers/images/", null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    submission_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Answer Id: {self.id} to the question {self.question}"
    
    @property
    def get_score(self):
        int_score = int(self.score)
        if int_score == self.score:
            return int_score
        return self.score
    




