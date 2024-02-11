from django.contrib import admin
from .models import Question, Choice
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["text"]}),
        ("Date information", {"fields": ["productiondate"]}),
    ]
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
# Register your models here.
#idididididididi