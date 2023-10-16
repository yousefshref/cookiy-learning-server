from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.UserProfile)


@admin.action(description='save')
def save(modeladmin, request, q):
    for i in q:
        i.save()

class CourseAdmin(admin.ModelAdmin):
    actions = [save]
admin.site.register(models.Course, CourseAdmin)


admin.site.register(models.Specialy)


admin.site.register(models.FavCourse)


admin.site.register(models.CourseReview)


admin.site.register(models.Enrollmment)