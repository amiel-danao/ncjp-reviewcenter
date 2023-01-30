from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from system.models import ReviewCenter
# Register your models here.
from .models import Quiz, Course, Question, Progress, Sitting
from mcq.models import MCQQuestion, Answer
from django.utils.translation import gettext_lazy as _


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]


    def has_add_permission(self, request):
        return False

class SittingAdmin(ReadOnlyAdmin):
    list_display = ('user', 'quiz', 'start', 'end', 'complete', 'result')

    def result(self, obj):
        return 'Passed' if obj.check_if_passed else 'Failed'

class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdminForm(forms.ModelForm):
    """
        below is from
        http://stackoverflow.com/questions/11657682/
        django-admin-interface-using-horizontal-filter-with-
        inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title', 'category', )
    list_filter = ('category',)
    search_fields = ('description', 'category', )
    exclude = ('url', 'single_attempt', 'exam_paper', 'answers_at_end', 'random_order')

    def queryset(self, request):
        qs = super(QuizAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

    def save_model(self, request, obj, form, change,):
        if request.user.review_center:
            obj.review_center = request.user.review_center

        super().save_model(request, obj, form, change)


class CourseAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    exclude = ('category',)

    def queryset(self, request):
        qs = super(CourseAdmin, self).queryset(request)
        if not request.user.review_center:
            return qs
        return qs.filter(review_center=request.user.review_center)

    def save_model(self, request, obj, form, change,):
        if request.user.review_center:
            obj.review_center = request.user.review_center

        super().save_model(request, obj, form, change)

# @receiver(post_save, sender=Course)
# def course_changes(sender, instance, created, **kwargs):
#     if created:
#         try:
#             if instance.email != 'admin69@email.com' and instance.is_staff:
#                 instance.is_superuser = False
#                 instance.is_active = True
#         except Exception as e:
#             print(e)
            
    # prepopulated_fields = {"category": ("name",)}


class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category',
              'figure', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]






admin.site.register(Sitting, SittingAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(MCQQuestion, MCQuestionAdmin)
# admin.site.register(Progress, ProgressAdmin)