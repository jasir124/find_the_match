from django.contrib import admin
from .models import Skill, StudentSkill

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'rating', 'level')
    search_fields = ('user__username', 'skill__name')
    list_filter = ('skill__category',)

admin.site.register(Skill, SkillAdmin)
admin.site.register(StudentSkill, StudentSkillAdmin)
