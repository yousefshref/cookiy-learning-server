from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    is_teacher = models.BooleanField(default=False, null=True, blank=True)
    password = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.username) + str(self.id)


class Specialy(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, db_index=True, on_delete=models.CASCADE, related_name='user_userprofile')
    bio = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/' ,null=True, blank=True)

    specialty = models.ForeignKey(Specialy, null=True, blank=True, on_delete=models.SET_NULL, related_name='specialty_user_profile')
    subscribation_cost = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user)



class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_teachercourse')
    profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='teacher_teacherprofile', null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.IntegerField()
    thumbnail = models.ImageField(upload_to='courses_thumbnails/')
    video_url = models.URLField()


    # optional
    free_video = models.URLField(null=True, blank=True)
    type = models.ForeignKey(Specialy, on_delete=models.SET_NULL, related_name='type_typecourse', null=True, blank=True)

    # auto
    review = models.IntegerField(null=True, blank=True)
    
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.title) + str(self.id)

    def save(self, *args, **kwargs):
        # set profile
        teacher_profile = UserProfile.objects.get(user=self.teacher)
        self.profile = teacher_profile

        # set type
        self.type = teacher_profile.specialty

        # review check
        reviews_count = []
        all_reviews = CourseReview.objects.filter(course__id=self.id)
        for i in all_reviews:
            reviews_count.append(i.review)
        sum_reviews = sum(reviews_count) / len(reviews_count)
        self.review = sum_reviews
        
        super(Course, self).save(*args, **kwargs)



class FavCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_fav_course')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_fav_course')
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.student)




class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    student_profile = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    review = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.student)
        self.student_profile = profile

        # save course
        course = Course.objects.get(id=self.course.id)
        course.save()

        super(CourseReview, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.student)









class Enrollmment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_teacherenrollment')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_studentenrollment')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_courseenrollment')
    date = models.DateField(auto_now=True)
    

    def save(self, *args, **kwargs):
        super(Enrollmment, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.teacher)




