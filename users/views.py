from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from .models import Classroom, Activity, Lesson, PassActivity
from django.contrib.auth.decorators import login_required
# Create your views here.


def about(request):
    return render(request, 'about.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('homepage')

def homepage(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect('teacher_dashboard') 
            
            elif user.is_staff:
                return redirect('student_dashboard')
            
            else:
                messages.error(request, "Please Wait for Admin to Approve your account")
                return redirect('homepage')
            
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('homepage')
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        fullname = request.POST['fname']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password1']
        repeat_password = request.POST['password2']
       
        if password != repeat_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('register')

        else:
            # Create new user
            user = User.objects.create_user(first_name=fullname, username=email, email=email, password=password, last_name=role)
            user.save()
            messages.success(request, 'You have been registered successfully.')
            return redirect('homepage')
    return render(request, 'register.html')





def classlist(request):
    # Get the currently authenticated user
    current_user = request.user
    
    # Query classrooms where the instructor is the current user
    classrooms = Classroom.objects.filter(instructor=current_user)
    
    # Create a context to pass to the template
    context = {
        'classrooms': classrooms,
    }
    return render(request, 'teacher/classlist.html',context)

@login_required
def remove_student(request, classroom_id, student_id):
    classroom = get_object_or_404(Classroom, id=classroom_id, instructor=request.user)
    student = get_object_or_404(User, id=student_id)
    
    if student in classroom.students.all():
        classroom.students.remove(student)
    
    return redirect('classlist')

@login_required(login_url='/homepage')
def teacher_dashboard(request):
    classroom = Classroom.objects.filter(instructor=request.user).order_by('-id')
    if request.method == 'POST':
        class_name = request.POST['class_name']
        section = request.POST['section']
        subject = request.POST['subject']
        room_code = request.POST['room_code']
        
        new_class = Classroom.objects.create(class_name=class_name, section=section, subject=subject, 
                                             instructor=request.user, room_code=room_code)
        new_class.save()
        messages.success(request, 'Classroom created')
        
    context = {
        'classroom':classroom,
    }
    return render(request, 'teacher/index.html', context)


def deleteClassroom(request, class_id):
    Classroom.objects.filter(id=class_id).delete()
    messages.success(request, 'Classroom Removed')
    return redirect('teacher_dashboard')

@login_required(login_url='/homepage')
def classroom(request, class_code):
    room = get_object_or_404(Classroom, room_code=class_code)
    classroom = Classroom.objects.filter(room_code=class_code)
    activity = Activity.objects.filter(room=room.id).order_by('-id')
    lessons = Lesson.objects.filter(classroom=room.id)
   
   
    # Iterate through activities to get PassActivity objects
    submissions = []
    for activities in activity:
        submission = PassActivity.objects.filter(activity_name=activities.id)
        submissions.extend(submission)
        
    if request.method == 'POST':
        if 'submit_form_one' in request.POST:
            label = request.POST['label']
            discussion = request.POST['discussion']
            deadline = request.POST['deadline']
            
            
            new_activity = Activity.objects.create(room=room, title=label, description=discussion, 
                                                   deadline=deadline)
            new_activity.save()
            messages.success(request, 'Activity Added')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        elif 'submit_form_two' in request.POST:
            title = request.POST['title']
            description = request.POST['lesson_discussion']
            lesson_file = request.FILES['lesson_file']
            
            new_lesson = Lesson.objects.create(title=title, description=description, lesson_file=lesson_file,
                                                classroom=room, teacher=request.user)
            new_lesson.save()
            messages.success(request, 'Lesson Added')
    context = {
        'classroom': classroom,
        'room': room,
        'activity':activity,
        'submissions': submissions,
        'lessons':lessons,
    }
    return render(request, 'teacher/classroom.html', context)

def deleteActivity(request, act_id):
    Activity.objects.filter(id=act_id).delete()
    messages.success(request, 'Activity Removed')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def deleteLesson(request, lesson_id):
    Lesson.objects.filter(id=lesson_id).delete()
    messages.success(request, 'Lesson Removed')
    return redirect(request.META.get('HTTP_REFERER', '/'))



def pass_activity(request, act_id):
    activity = get_object_or_404(Activity, id=act_id)
    activity_submission = PassActivity.objects.filter(activity_name=activity)
    
    if request.method == 'POST':
        # Retrieve the score from the form data
        score = request.POST.get('score')

        # Update the scores for each submission
        for submission in activity_submission:
            submission.score = score
            submission.save()
            messages.success(request, 'Score Recorded')
        # Optionally, you can redirect the user to a different page
        return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'activity': activity,
        'activity_submission': activity_submission,
    }
    return render(request, 'teacher/pass_activity.html', context)









def student_dashboard(request):
    
    classroom_id = request.GET.get('classroom_id')
    room_code = request.GET.get('room_code')
    
    if 'search' in request.GET:
        search_query = request.GET['search']
        # Perform case-insensitive search using room_code
        matching_classrooms = [classroom for classroom in Classroom.objects.all() if classroom.verify_room_code(search_query)]
    else:
        matching_classrooms = []
    
    
    if classroom_id and room_code:
        # Retrieve the classroom instance
        classroom = get_object_or_404(Classroom, id=classroom_id)

        # Verify if the entered room code matches the classroom's room code
        if classroom.verify_room_code(room_code):
            # Add the current user (student) to the classroom
            classroom.students.add(request.user)
            messages.success(request, 'You have successfully joined the classroom go to Classes section.')
        else:
            # Display an error message if the room code is incorrect
            messages.error(request, 'Incorrect room code. Unable to join classroom.')
    
    context = {
        'classrooms': matching_classrooms
    }
    return render(request, 'student/index.html', context)



def student_classroom(request):
    classroom = Classroom.objects.filter(students=request.user).order_by('-id')
    
    context = {
        'classroom': classroom,
    }
    return render(request, 'student/classroom.html', context)


def student_room(request, class_code):
    room = get_object_or_404(Classroom, room_code=class_code)
    activities = Activity.objects.filter(room=room.id)
    lesson = Lesson.objects.filter(classroom=room)
    
    if request.method == 'POST':
        file = request.FILES['file']
        activity_id = request.POST.get('activity_id')  
        activity_instance = get_object_or_404(Activity, pk=activity_id)
        
        if activity_instance.user_has_submitted_file(request.user):
            messages.error(request, 'You have already submitted a file for this activity.')
        else:
            new_submission = PassActivity.objects.create(activity_name=activity_instance, file=file, submitBy=request.user, score=0)
            new_submission.save()
            messages.success(request, 'Submitted Successfully.')
 
    context = {
        'room': room,
        'activities': activities,
        'lessons':lesson,
       
    }
    return render(request, 'student/room.html', context)





def mainLogin(request):
    return render(request, 'main/mainLogin.html')

def dashboard(request):
    student = User.objects.filter(last_name='Student').order_by('-id')
    instructor = User.objects.filter(last_name='Teacher').order_by('-id')
    context = {
        'student': student,
        'instructor':instructor
       
    }
    return render(request, 'main/mainDashboard.html', context)



def approve_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = True
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')

def disapprove_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = False
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')


def approve_instructor(request, instructor_id):
    user = User.objects.get(pk=instructor_id)
    user.is_superuser = True
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')

def disapprove_instructor(request, instructor_id):
    user = User.objects.get(pk=instructor_id)
    user.is_superuser = False
    user.save()
    # You can redirect to a success page or to the same page
    return redirect('mainDashboard')


def deleteUser(request, user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'User Removed')
    return redirect('/mainDashboard')




def forum(request):
    context = {
        'user': request.user
    }
    return render(request, 'teacher/forum.html', context)


def student_forum(request):
    
    context = {
        'user': request.user
    }
    return render(request, 'student/forum.html', context)