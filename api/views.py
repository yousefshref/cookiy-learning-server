from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models
from . import serializers
from django.core.paginator import Paginator
from django.db.models import Q




@api_view(['GET'])
def get_specialies(request):
    specialies = models.Specialy.objects.all()
    ser = serializers.SpecialySerializer(specialies, many=True)
    return Response(ser.data)



# REGISTERATION
@api_view(['POST'])
def register(request):
    username = request.data['username']
    email = request.data['email']
    is_teacher = request.data.get('is_teacher')
    password = request.data['password']

    # check username
    if len(username) == 0:
        return Response({"username":"يجب ان تكتب اسم مستخدم"})

    if len(username) > 50:
        return Response({"username":"اسم المستخدم يجب ان يكون اقل من 50 حرف"})

    try:
        exist_username = models.User.objects.get(username=username)
        return Response({"username":"هذا الاسم موجود بالفعل, يرجي استخدام اسم اخر"})
    except:
        pass

    # check email
    try:
        email_split = email.split('@')
        if email_split[1] != 'gmail.com':
            return Response({"email":"يجب ان يحتوي علي @gmail.com"})
    except:
        return Response({"email":"يجب علي البريد الالكتروني ان يحتوي علي @gmdil.com"})

    try:
        exist_email = models.User.objects.get(email=email)
        return Response({"email":"هذا البريد الالكتروني مسجل بالفعل"})
    except:
        pass

    # check type
    if len(is_teacher) == 0:
        return Response({"type":"يجب ان تختار نوع حسابك"})

    # check password
    if len(password) == 0:
        return Response({"password":"يجب ان تكتب كلمة السر"})

    if len(password) > 255:
        return Response({"كلمة السر يجب ان تكون اقل من 255 حرف"})


    create_user = models.User(
        username=username,
        email=email,
        is_teacher=is_teacher,
        password=password,
    ).save()


    # create_profile
    user = models.User.objects.get(email=email)
    create_profile = models.UserProfile(
        user_id=user.pk
    ).save()

    return Response({"success":True})


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    # check email
    try:
        email_split = email.split('@')
        if email_split[1] != 'gmail.com':
            return Response({"email":"يجب ان يحتوي علي @gmail.com"})
    except:
        return Response({"email":"يجب علي البريد الالكتروني ان يحتوي علي @gmdil.com"})

    # check password
    if len(password) == 0:
        return Response({"password":"يجب ان تكتب كلمة السر"})
    if len(password) > 255:
        return Response({"كلمة السر يجب ان تكون اقل من 255 حرف"})


    # check login
    try:
        exist_user = models.User.objects.get(email=email)
        if exist_user.password == password:
            return Response({"success":True})
        else:
            return Response({"password":"كلمة المرور غير صالحة"})
    except:
        return Response({"error":"لا يوجد حساب بهذا البريد"})




# PROFILE
@api_view(['GET'])
def get_user_profile(request):
    user = models.User.objects.get(email=request.GET.get('email'))
    profile = models.UserProfile.objects.get(user__id=user.pk)
    ser = serializers.UserProfileSerializer(profile)
    return Response(ser.data)


@api_view(['GET'])
def get_teacher_profile(request):
    id = request.GET.get('id')
    profile = models.UserProfile.objects.get(user__id=id, user__is_teacher=True)
    ser = serializers.UserProfileSerializer(profile)
    return Response(ser.data)



@api_view(['POST'])
def edit_profile(request):
    user_email = request.data['email']
    bio = request.data.get('bio')
    image = request.FILES.get('image')

    specialty = request.data.get('specialty')
    subscribation_cost = request.data.get('subscribation_cost')

    user = models.UserProfile.objects.get(user__email=user_email)

    if bio:
        if len(bio) == 0:
            return Response({"bio":"يجب ان تكتب وصف"})
        else:
            user.bio = bio
            user.save()


    if image:
        user.image = image
        user.save()


    try:
        spe = models.Specialy.objects.get(id=specialty)
    except:
        pass

    if specialty:
        user.specialty = spe
        user.save()
        # user.specialty = specialty
        # user.specialty.save()
        # user.save()


    if subscribation_cost:
        if int(subscribation_cost) <= 0:
            return Response({"subscribation_cost":"يجب ان تكتب سعر مناسب"})

        user.subscribation_cost = subscribation_cost
        user.save()



    return Response({"success":True})




# COURSE
@api_view(['POST'])
def create_course(request):
    teacher_email = request.data['teacher_email']
    title = request.data['title']
    description = request.data['description']
    price = request.data['price']
    thumbnail = request.FILES.get('thumbnail')
    video_url = request.data['video_url']

    free_video = request.data.get('free_video')

    # checl title
    if len(title) == 0:
        return Response({"title":"يجب علي الاسم ان يكون مكتوب"})
    if len(title) > 150:
        return Response({"title":"يجب علي الاسم ان يكون اقل من 150 حرف"})

    # checl description
    if len(description) == 0:
        return Response({"description":"يجب ان تكتب وصف"})


    # checl price
    if len(price) == 0:
        return Response({"price":"يجب ان تكتب السعر"})

    if price.isnumeric():
        pass
    else:
        return Response({"price":"يجب علي السعر ان يكون ارقام فقط"})


    # checl thumbnail
    try:
        if len(thumbnail) == 0:
            return Response({"thumbnail":"يجب ان تضع صورة"})
    except:
        return Response({"thumbnail":"يجب ان تضع صورة مصغرة"})

        
    # checl video
    if len(video_url) == 0:
        return Response({"video":"يجب ان تضع رابط الفديو"})


    user = models.User.objects.get(email=teacher_email)
    
    create_create = models.Course(
        teacher=user,
        title=title,
        description=description,
        price=price,
        thumbnail=thumbnail,
        video_url=video_url,
        free_video=free_video,
    ).save()


    return Response({"success":True})



@api_view(['GET'])
def get_teacher_courses(request):
    email = request.GET.get('email')
    id = request.GET.get('id')
    teacher_id = request.GET.get('teacher_id')


    courses = models.Course.objects.filter(teacher__email=email).order_by('-id')
    
    title = request.GET.get('title')

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if title:
        courses = courses.filter(title__icontains=title)

    if date_from and date_to:
        courses = courses.filter(date__range=[date_from, date_to])




    if id:
        course = models.Course.objects.get(id=id, teacher__email=email)
        ser = serializers.CourseSerializer(course)
        return Response(ser.data)


    if teacher_id:
        course = models.Course.objects.filter(teacher__id=teacher_id)
        ser = serializers.CourseSerializer(course.order_by('-id'), many=True)
        return Response(ser.data)


    

    paginator = Paginator(courses, 15)
    page_number = request.GET.get('page_number')
    page_obj = paginator.get_page(page_number)
    paginated_products = page_obj.object_list

    serializer = serializers.CourseSerializer(paginated_products, many=True)
    data = {
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }
    return Response(data)



@api_view(['POST'])
def edit_teacher_course(request):
    email = request.data.get('email')
    course_id = request.data.get('course_id')

    course = models.Course.objects.get(teacher__email=email, id=course_id)

    # data
    title = request.data.get('title')
    description = request.data.get('description')
    price = request.data.get('price')
    thumbnail = request.FILES.get('thumbnail')
    video_url = request.data.get('video_url')

    free_video = request.data.get('free_video')

    # checl title
    if len(title) == 0:
        return Response({"title":"يجب علي الاسم ان يكون مكتوب"})
    if len(title) > 150:
        return Response({"title":"يجب علي الاسم ان يكون اقل من 150 حرف"})

    # checl description
    if len(description) == 0:
        return Response({"description":"يجب ان تكتب وصف"})


    # checl price
    if len(price) == 0:
        return Response({"price":"يجب ان تكتب السعر"})

    if price.isnumeric():
        pass
    else:
        return Response({"price":"يجب علي السعر ان يكون ارقام فقط"})

        
    # checl video
    if len(video_url) == 0:
        return Response({"video":"يجب ان تضع رابط الفديو"})


    if title != course.title:
        course.title = title

    if description != course.description:
        course.description = description

    if price != course.price:
        course.price = price

    if thumbnail == None:
        pass
    else:
        course.thumbnail = thumbnail

    if video_url != course.video_url:
        course.video_url = video_url

    if free_video != course.free_video:
        course.free_video = free_video
    
    course.save()


    return Response({"success":True})



@api_view(['DELETE'])
def delete_course(request):
    email = request.GET.get('email')
    id = request.GET.get('id')

    course = models.Course.objects.get(teacher__email=email, id=id)
    course.delete()

    return Response({"success":True})




@api_view(['GET'])
def get_all_courses(request):
    courses = models.Course.objects.all().order_by('-review')
    q = request.GET.get('q')
    id = request.GET.get('id')

    teacher_id = request.GET.get('teacher_id')

    if teacher_id:
        courses = courses.filter(teacher__id=teacher_id)

    if id:
        courses = courses.filter(id=id)


    if q:
        words = q.split(' ')
        q_objects = [Q(title__icontains=word) | Q(description__icontains=word) for word in words]

        combined_q_object = Q()
        for q_object in q_objects:
            combined_q_object |= q_object

        courses = courses.filter(combined_q_object).order_by('-review')

    

    paginator = Paginator(courses, 20)
    page_number = request.GET.get('page_number')
    page_obj = paginator.get_page(page_number)
    paginated_products = page_obj.object_list

    serializer = serializers.CourseSerializer(paginated_products, many=True)
    data = {
        'results': serializer.data,
        'total_pages': paginator.num_pages,
        'current_page': page_obj.number,
    }
    return Response(data)






# FAVOURET COURSE
@api_view(['POST'])
def add_to_fav(request):
    student = request.data['student']
    course = request.data['course']

    # check exist
    try:
        exist = models.FavCourse.objects.get(student__id=student, course__id=course)
        return Response({"exist":True})
    except:
        models.FavCourse(
            student_id=student,
            course_id=course
        ).save()

    return Response({"success":True})


@api_view(['GET'])
def get_student_fav(request):
    student = request.GET.get('student')

    saved = models.FavCourse.objects.filter(
        student__id=student
    )

    ser = serializers.FavCourseSerializer(saved, many=True)
    return Response(ser.data)



@api_view(['DELETE'])
def delete_from_fav(request):
    fav_id = request.GET.get('fav_id')
    student = request.GET.get('student')

    print(fav_id)
    print(student)

    models.FavCourse.objects.get(
        course__id=fav_id,
        student__id=student
    ).delete()
    
    return Response({"success":True})



@api_view(['DELETE'])
def delete_all_fav(request):
    student = request.GET.get('student')

    favs = models.FavCourse.objects.filter(student__id=student)

    for fav in favs:
        fav.delete()
    
    return Response({"success":True})





# COURSE REVIEW
@api_view(['POST'])
def create_course_review(request):
    course = request.data['course']
    student = request.data['student']
    review = request.data.get('review')
    comment = request.data.get('comment')

    models.CourseReview(
        course_id=course,
        student_id=student,
        review=review,
        comment=comment
    ).save()

    return Response({"success":True})



@api_view(['POST'])
def update_course_review(request):
    course = request.data['course']
    student = request.data['student']
    review = request.data.get('review')
    comment = request.data.get('comment')
    reply = request.data.get('reply')

    try:
        exist = models.CourseReview.objects.get(
            course_id=course,
            student_id=student,
        )
        exist.review = review
        exist.comment = comment
        exist.reply = reply
        exist.save()
        return Response({"success":True})
    except:
        return Response({"not_exist":"حدث خطأ لا يوجد تقييم موجود بهذه المعلومات"})
    



@api_view(['GET'])
def get_course_review(request):
    course = request.GET.get('course')

    reviews = models.CourseReview.objects.filter(
        course_id=course
    )

    ser = serializers.CourseReviewSerializer(reviews.order_by('-review'), many=True)

    return Response(ser.data)



    



# ENROLLMENTS
@api_view(['GET'])
def get_enrollments(request):
    student = request.GET.get('student')

    # studnet enrollments
    enrollments = models.Enrollmment.objects.filter(student__id=student)
    ser = serializers.EnrollmmentSerializer(enrollments.order_by('-date'), many=True)
    return Response(ser.data)









