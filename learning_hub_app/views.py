from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User,Course,Subject,Chapter,Assignment,AssignmentSubmission
from django.db import IntegrityError



User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone_no")
        role = request.POST.get("role")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # ----------------- Validation -----------------
        if not username or not email or not password1 or not password2 or not role:
            messages.error(request, "Please fill in all required fields.")
            return redirect("signup")

        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:    
            user = User.objects.create_user(
            username=username,
            email=email,
            phone_no=phone_no,  
            role=role,
            password=password1
          )
            user.save()

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    return render(request, 'sign_up.html')
        
# ------------------ LOGIN VIEW ------------------
def user_login(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request,"invalid email or password")
            return redirect("login")
        
        user = authenticate(request,username=username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is inactive")
                return redirect("login")
            login(request, user)
            


            # Redirect based on role
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "teacher":
                return redirect("teacher_dashboard")
            elif user.role == "admin":
                return redirect("admin_dashbord.html")
            else:
                messages.error(request, "Invalid role assigned.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")

# ------------------ LOGOUT VIEW ------------------
def user_logout(request):
    logout(request)
    return redirect("login")

# ------------------ DASHBOARD VIEWS ------------------
@login_required
def student_dashboard(request):
    return render(request, "student/student_dashboard.html")

@login_required
def teacher_dashboard(request): 
    courses = Course.objects.all()       # <-- add this
    total_courses = courses.count()     # <-- count from queryset
    total_students = User.objects.filter(role="student").count()
    total_assignments = Assignment.objects.count()

    return render(request, "teacher/teacher_dashboard.html", {
        'total_courses': total_courses,
        'course': courses,     # <-- send course 
        'total_students': total_students,
        'total_assignments' : total_assignments,
    })                
   

@login_required
def admin_dashboard(request):
    return render(request, "admin/admin_dashbord.html")

########------course model------########

def courses_list(request):
    all_course = Course.objects.all()
    return render(request,'teacher/course_list.html',{'course':all_course})

def add_course(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        instructor = request.POST.get('instructor')

        if title and description and instructor:
            Course.objects.create(title=title, description=description, instructor=instructor)
            messages.success(request, "Course added successfully!")
            return redirect('courses_list')
        else:
            messages.error(request, "Please fill all fields.")

    return render(request, 'teacher/add_course.html')

def course_detail(request,id):
    one_course = get_object_or_404(Course, id=id)
    return render(request,'teacher/course_detail.html',{'d':one_course})

def delete_course(request,id):
    dc = Course.objects.get(id=id)
    dc.delete()
    return redirect('courses_list')

def edit_course(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        instructor = request.POST.get('instructor')

        if title and description and instructor:
            course.title = title
            course.description = description
            course.instructor = instructor
            course.save()
            messages.success(request, "Course updated successfully!")
            return redirect('courses_list')
        else:
            messages.error(request, "Please fill all fields.")

    return render(request, 'teacher/edit_course.html', {'course': course})

#---------------SUBJECT MODELS----------------#
# list all subject:
def subject_list(request):
    subjects = Subject.objects.select_related('course').all()
    return render(request, "teacher/subject_list.html", {'s': subjects,'course': None,})

def subject_add(request):
    courses = Course.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        course_id = request.POST.get('course')

        course = get_object_or_404(Course, id=course_id)
        Subject.objects.create(name=name, code=code, course=course, description=description,)
        messages.success(request, "Subject added successfully!")
        return redirect('subject_list')

    return render(request, 'teacher/add_subject.html', {'a': courses})

# update a subject
def subject_update(request,id):
    subject = get_object_or_404(Subject,id=id)
    courses = Course.objects.all()

    if request.method == "POST":
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        subject.description = request.POST.get('description')
        course_id = request.POST.get('course')
        subject.course = get_object_or_404(Course, id=course_id)
        
        try:
            subject.save()
            messages.success(request, "Subject updated successfully!")
            return redirect('subject_list')
        except IntegrityError:
            messages.error(request, "Subject code must be unique. This code already exists.")
    
    return render(request, "teacher/update_subject.html",{'subject':subject,'u':courses})

def subject_delete(request,id):
    ds = Subject.objects.get(id=id)
    ds.delete()
    return redirect('subject_list')

#----------------Chapter model----------------#
#list of chapters
def chapter_list(request):
    chapters = Chapter.objects.select_related('subject').all()
    return render(request,'teacher/chapter_list.html',{'chapters':chapters})

def chapter_add(request):
    subjects = Subject.objects.all()
    if request.method == "POST":
        subject_id = request.POST.get('subject')
        number = request.POST.get('number')
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')

        subject = get_object_or_404(Subject,id=subject_id)
        Chapter.objects.create(title=title,number=number,subject=subject,description=description,content=content)
        messages.success(request,"Chapeter added successfully")
        return redirect('chapters')
    
    return render(request,"teacher/chapter_add.html",{'subjects': subjects})

def chapter_update(request,id):
    chapter = get_object_or_404(Chapter,id=id)
    subjects = Subject.objects.all()

    if request.method == "POST":
        subject_id = request.POST.get('subject')
        chapter.subject =get_object_or_404(Subject, id=subject_id)
        chapter.title = request.POST.get('title')
        chapter.number = request.POST.get('number')
        chapter.description = request.POST.get('description')
        chapter.content = request.POST.get('content')
        chapter.save()
        messages.success(request,"chapter updated successfully!")
        return redirect('chapters')
    
    return render(request,"teacher/chapter_update.html",{'chapter':chapter,'subjects':subjects})

def chapter_detail(request,id):
    chapter = get_object_or_404(Chapter,id=id)
    return render(request,"teacher/chapter_detail.html",{'chapter':chapter})

def chapter_delete(request,id):
    chapter = get_object_or_404(Chapter,id=id)
    chapter.delete()
    messages.success(request,"chapter deleted successfully!")
    return redirect('chapters')

    

#----------------assignments model-------------#
def assignment_list(request):
    assignments = Assignment.objects.select_related('chapter').all()
    return render(request,'assignments/assignments_list.html',{'assignments': assignments})

def assignment_add(request):
    chapters = Chapter.objects.all()

    if request.method == "POST":
        chapter_id = request.POST.get('chapter')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        marks = request.POST.get('marks')
        file = request.FILES.get('file')
        chapter = get_object_or_404(Chapter, id=chapter_id)

        Assignment.objects.create(
            chapter=chapter,
            title= title,
            description= description,
            due_date = due_date,
            marks = marks,
            file = file
        )
        messages.success(request,"Assignment created successfully!")
        return redirect('assignment_list')
    
    return render(request,"assignments/add_assignments.html",{'chapters':chapters})

def assignment_detail(request,id=id):
    assignment = get_object_or_404(Assignment, id=id)
    return render(request,"assignments/detail_assignments.html",{"assignment":assignment})

def assignment_update(request,id):
    assignment = get_object_or_404(Assignment,id=id)
    chapters = Chapter.objects.all()

    if request.method == "POST":
        assignment.chapter = get_object_or_404(Chapter,id=request.POST.get('chapter'))
        assignment.title = request.POST.get('title')
        assignment.description = request.POST.get('description')
        assignment.due_date = request.POST.get('due_date')
        assignment.marks = request.POST.get('marks')

        if request.POST.get('file'):
            assignment.file = request.POST.get('file')
        assignment.save()
        messages.success(request,"Assignment updated successfully!")
        return redirect('assignment_list')
    return render(request,"assignments/assignment_update.html",{'assignment':assignment,'chapters':chapters})

def assignment_delete(request,id):
    assignment = get_object_or_404(Assignment,id=id)
    assignment.delete()
    messages.success(request,"Assignment deleted successfully!")
    return redirect('assignment_list')

#------------------Assignment-Submission-----------------------#
@login_required
def submission_list(request):
    if request.user.role == 'teacher':
        submissions = AssignmentSubmission.objects.select_related('assignment','student').all()
    else:
        submissions = AssignmentSubmission.objects.filter(student=request.user).select_related('assignment')
    return render(request,"submissions/submission_list.html",{'submissions':submissions})

@login_required
def submission_add(request,assignment_id):
    assignment = get_object_or_404(Assignment,id=assignment_id)

    existing = AssignmentSubmission.objects.filter(assignment=assignment,student=request.user).first()
    if existing:
        messages.info(request, "you already submitted this assignment. you can update it instead")
        return redirect('submission_view',id=existing.id)
    
    if request.method == "POST":
        answer_text = request.POST.get('answer_text')
        file = request.FILES.get('file')
        today = timezone.now().date()
        if assignment.due_date and today > assignment.due_date:
            status = 'late'
        else:
            status = 'on_time'

        sub = AssignmentSubmission.objects.create(
            assignment = assignment,
            student = request.user,
            answer_text = answer_text,
            file = file,
            status = status)
        messages.success(request, "Assignment submitted successfully!")
        return redirect('submission_view', id=sub.id)
    
    return render(request, "submissions/submission_add.html",{'assignment':assignment})

def submission_view(request,id):
    submission = get_object_or_404(AssignmentSubmission,id=id)
    if request.user.role != 'teacher' and submission.student != request.user:
        messages.error(request,"you don't have permission to view this assignment")
        return redirect('submissions')
    
    return render(request,"submissions/submission_view.html",{'submission':submission})

@login_required
def submission_update(request,id):
    submission = get_object_or_404(AssignmentSubmission, id=id)
    assignment = submission.assignment

    if submission.student != request.user:
        messages.error(request,"you don't have permission to edit this assignment")
        return redirect('submissions')
    
    if submission.mark_awarded is not None:
        messages.warning(request,"this submiision has been graded and you cannot be edited")
        return redirect('submission_view', id=submission.id)
    
    if request.method == "POST":
        submission.answer_text = request.POST.get('answer_text')
        if request.FILES.get('file'):
            submission.file == request.FILES.get('file')

        submission.submitted_at = timezone.now()
        today = timezone.now().date()
        if assignment.due_date and today > assignment.due_date:
            submission.status == 'late'
        else:
            submission.status == 'on_time'

        submission.save()
        messages.success(request,"Submission updated")
        return redirect('submission_view', id=submission.id)
    
    return render(request,"submissions/submission_update.html",{'submission':submission})

@login_required
def submission_grade(request, id):
    if request.user.role != 'teacher':
        messages.error(request,"only teachers can grade submissions.")
        return redirect('submissions')
    
    submission = get_object_or_404(AssignmentSubmission, id=id)

    if request.method == "POST":
        marks = request.POST.get('mark_awarded')
        feedback = request.POST.get('feedback')

        submission.mark_awarded = int(marks) if marks not in (None,'') else None
        submission.feedback = feedback
        submission.graded_by = request.user
        submission.graded_at = timezone.now()
        submission.save()
        messages.success(request,"Submission graded")
        return redirect('submission_view', id=submission.id)
    
    return render(request,"submissions/submission_grade.html",{'submission':submission})

@login_required
def submission_delete(request,id):
    submission = get_object_or_404(AssignmentSubmission, id=id)

    if not(request.user.role == 'teacher' or submission.student == request.user):
        messages.error(request,"you don't have permission to delete this submission")
        return redirect('submissions')
    
    submission.delete()
    messages.success(request,"submission deleted")
    return redirect('submissions')

# Create your views here.

def BASE(request):
    return render(request, 'index.html')
# def BASET(request):
#     return render(request, 'teacher/teacher_dashboard.html')
def BASES(request):
    return render(request, 'student/index.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def sign_in(request):
    return render(request, 'sign_in.html')