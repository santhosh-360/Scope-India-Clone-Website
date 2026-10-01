from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, StudentForm
from .models import Student, Course, Enrollment

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

import uuid
import random
import string


# HOME

def home(request):
    return render(request, 'home.html')


# COURSES PAGE


def courses(request):

    courses = Course.objects.all()

    return render(
        request,
        'courses.html',
        {
            'courses': courses
        }
    )


# ABOUT

def about(request):
    return render(request, 'about.html')


# CONTACT

def contact(request):

    message = ""

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            contact = form.save()

            try:

                send_mail(
                    subject=contact.subject,

                    message=f"""
Name: {contact.name}
Email: {contact.email}
Message: {contact.message}
""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[
                        'santhoshrs360@gmail.com'
                    ],

                    fail_silently=False
                )

                message = "Your Email has been sent successfully."

            except Exception:

                
                message = (
                    "Unable to send email right now. "
                    "Please try again later."
                )

        else:

            message = "Please correct the errors in the form."

    else:

        form = ContactForm()

    return render(
        request,
        'contact.html',
        {
            'form': form,
            'message': message
        }
    )


# STUDENT REGISTRATION

def registartion(request):

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            student = form.save(commit=False)

            # Convert hobbies list into string
            hobbies = form.cleaned_data.get(
                'hobbies',
                []
            )

            student.hobbies = ', '.join(hobbies)

            # Create verification token
            student.verification_token = uuid.uuid4()

            # Save student
            student.save()

            # Create verification URL
            full_url = request.build_absolute_uri('/')

            verification_url = (
                f"{full_url}verify/"
                f"{student.verification_token}"
            )

            try:

                send_mail(
                    'SCOPE INDIA - Email Verification',

                    f"""
Hello {student.first_name},

Thank you for registering with SCOPE INDIA.

Please click the link below to verify your email:

{verification_url}

Thank you,
SCOPE INDIA
""",

                    settings.DEFAULT_FROM_EMAIL,

                    [student.email],

                    fail_silently=False
                )

                return render(
                    request,
                    'registartion.html',
                    {
                        'form': StudentForm(),
                        'success': (
                            'Registration successful! '
                            'Please check your email and click '
                            'the verification link.'
                        )
                    }
                )

            except Exception as e:

                print("Email Error:", e)
                return render(
                    request,
                    'registartion.html',
                    {
                        'form': form,
                        'error': (
                            'Registration saved, but we were '
                            'unable to send the verification email.'
                        )
                    }
                )

        else:

            return render(
                request,
                'registartion.html',
                {
                    'form': form
                }
            )

    else:

        form = StudentForm()

    return render(
        request,
        'registartion.html',
        {
            'form': form
        }
    )


# EMAIL VERIFICATION

def verify_email(request, token):

    try:

        student = Student.objects.get(
            verification_token=token
        )

    except Student.DoesNotExist:

        messages.error(
            request,
            'This verification link is invalid or has already expired.'
        )

        return render(
            request,
            'email_verified.html',
            {
                'invalid_link': True
            }
        )

    if student.email_verified:

        return render(
            request,
            'email_verified.html',
            {
                'student': student,
                'already_verified': True
            }
        )

    student.email_verified = True

    student.verification_token = uuid.uuid4()

    student.save(
        update_fields=[
            'email_verified',
            'verification_token'
        ]
    )

    return render(
        request,
        'email_verified.html',
        {
            'student': student
        }
    )


# LOGIN

def user_login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:

            student = Student.objects.get(
                email=email
            )

        except Student.DoesNotExist:

            messages.error(
                request,
                'Invalid email or password'
            )

            return render(
                request,
                'login.html'
            )

        # Check password
        if not check_password(
            password,
            student.password
        ):

            messages.error(
                request,
                'Invalid email or password'
            )

            return render(
                request,
                'login.html'
            )

        # Store Student ID in session
        request.session['student_id'] = student.id

        # Remember me
        if remember_me:

            request.session.set_expiry(
                60 * 60 * 24 * 30
            )

        else:

            request.session.set_expiry(0)

        # First login
        if student.is_first_login:

            return redirect(
                'create_new_password'
            )

        return redirect(
            'student_dashboard'
        )

    return render(
        request,
        'login.html'
    )

# CREATE NEW PASSWORD

def create_new_password(request):

    student_id = request.session.get(
        'student_id'
    )

    if not student_id:

        return redirect('login')

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        new_password = request.POST.get(
            'new_password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        if new_password != confirm_password:

            messages.error(
                request,
                'Passwords do not match.'
            )

            return render(
                request,
                'create_new_password.html'
            )

        if len(new_password) < 6:

            messages.error(
                request,
                'Password must contain at least 6 characters.'
            )

            return render(
                request,
                'create_new_password.html'
            )

        student.password = make_password(
            new_password
        )

        student.is_first_login = False

        student.save()

        return redirect('home')

    return render(
        request,
        'create_new_password.html'
    )

# STUDENT DASHBOARD

def student_dashboard(request):

    # Get logged-in Student ID
    student_id = request.session.get(
        'student_id'
    )

    if not student_id:

        return redirect('login')

    # Get Student
    student = get_object_or_404(
        Student,
        id=student_id
    )

    # Search courses
    search = request.GET.get(
        'search',
        ''
    )

    if search:

        courses = Course.objects.filter(
            course_name__icontains=search
        )

    else:

        courses = Course.objects.all()

    # Get courses picked by this Student
    picked_courses = Enrollment.objects.filter(
        student=student
    ).select_related(
        'course'
    )

    return render(
        request,
        'student_dashboard.html',
        {
            'student': student,
            'courses': courses,
            'picked_courses': picked_courses,
            'search': search
        }
    )

# SIGN UP / PICK COURSE

def signup_course(request, course_id):

    # Get logged-in Student ID
    student_id = request.session.get(
        'student_id'
    )

    if not student_id:

        return redirect('login')

    # Get Student
    student = get_object_or_404(
        Student,
        id=student_id
    )

    # Get selected Course
    course = get_object_or_404(
        Course,
        id=course_id
    )

    # Create enrollment
    # get_or_create prevents duplicate enrollment
    Enrollment.objects.get_or_create(
        student=student,
        course=course
    )

    # Return to dashboard
    return redirect(
        'student_dashboard'
    )


# REMOVE / UNPICK COURSE

def remove_course(request, course_id):

    # Get logged-in Student ID
    student_id = request.session.get(
        'student_id'
    )

    if not student_id:

        return redirect('login')

    # Get Student
    student = get_object_or_404(
        Student,
        id=student_id
    )

    # Remove selected course
    Enrollment.objects.filter(
        student=student,
        course_id=course_id
    ).delete()

    return redirect(
        'student_dashboard'
    )

# GENERATE PASSWORD

def generate_password(request):

    if request.method == 'POST':

        email = request.POST.get(
            'email'
        )

        try:

            student = Student.objects.get(
                email=email
            )

        except Student.DoesNotExist:

            messages.error(
                request,
                'Email address not found.'
            )

            return render(
                request,
                'generate_password.html'
            )

        # Student must verify email
        if not student.email_verified:

            messages.error(
                request,
                'Please verify your email before generating a password.'
            )

            return render(
                request,
                'generate_password.html'
            )

        # Generate temporary password
        temp_password = ''.join(
            random.choices(
                string.ascii_letters +
                string.digits,
                k=8
            )
        )

        # Hash password
        student.password = make_password(
            temp_password
        )

        student.is_first_login = True

        student.save()

        try:

            send_mail(
                'SCOPE INDIA - Temporary Password',

                f"""
Hello {student.first_name},

Your temporary password is:

{temp_password}

Please use this password to login to your SCOPE INDIA account.

After login, you will be asked to create a new password.

Thank you,
SCOPE INDIA
""",

                settings.DEFAULT_FROM_EMAIL,

                [student.email],

                fail_silently=False
            )

            return render(
                request,
                'generate_password.html',
                {
                    'success':
                        'Temporary password has been sent to your email.'
                }
            )

        except Exception as e:

            print("Email Error:", e)

            return render(
                request,
                'generate_password.html',
                {
                    'error':
                        'Unable to send email right now.'
                }
            )

    return render(
        request,
        'generate_password.html'
    )

# FORGOT PASSWORD

def forgot_password(request):

    if request.method == 'POST':

        email = request.POST.get(
            'email'
        )

        try:

            student = Student.objects.get(
                email=email
            )

        except Student.DoesNotExist:

            messages.error(
                request,
                'Email address not found.'
            )

            return render(
                request,
                'forgot_password.html'
            )

        # Generate temporary password
        temp_password = ''.join(
            random.choices(
                string.ascii_letters +
                string.digits,
                k=8
            )
        )

        student.password = make_password(
            temp_password
        )

        student.is_first_login = True

        student.save()

        try:

            send_mail(
                'SCOPE INDIA - Password Reset',

                f"""
Hello {student.first_name},

We received a request to reset your password.

Your temporary password is:

{temp_password}

Use this temporary password to login.

After login, you will be asked to create a new password.

Thank you,
SCOPE INDIA
""",

                settings.DEFAULT_FROM_EMAIL,

                [student.email],

                fail_silently=False
            )

            messages.success(
                request,
                'A temporary password has been sent to your email.'
            )

        except Exception:

            messages.error(
                request,
                'Unable to send email right now.'
            )

    return render(
        request,
        'forgot_password.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    request.session.flush()

    return redirect(
        'login'
    )

# PROFILE EDIT

def profile_edit(request):

    student_id = request.session.get(
        'student_id'
    )

    if not student_id:

        return redirect('login')

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        print("FORM ERRORS:", form.errors)

        if form.is_valid():

            student = form.save(
                commit=False
            )

            hobbies = form.cleaned_data.get(
                'hobbies',
                []
            )

            student.hobbies = ', '.join(
                hobbies
            )

            student.save()

            print("STUDENT SAVED")

            return redirect(
                'profile_edit'
            )

    else:

        if student.hobbies:

            initial_hobbies = (
                student.hobbies.split(', ')
            )

        else:

            initial_hobbies = []

        form = StudentForm(
            instance=student,
            initial={
                'hobbies': initial_hobbies
            }
        )

    return render(
        request,
        'profile_edit.html',
        {
            'form': form,
            'student': student
        }
    )

# CHANGE PASSWORD

def change_password(request):

    student_id = request.session.get(
        'student_id'
    )

    if not student_id:

        return redirect('login')

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == 'POST':

        existing_password = request.POST.get(
            'existing_password'
        )

        new_password = request.POST.get(
            'new_password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )

        # Check old password
        if not check_password(
            existing_password,
            student.password
        ):

            messages.error(
                request,
                'Existing password is incorrect.'
            )

            return render(
                request,
                'change_password.html'
            )

        # Check new password
        if new_password != confirm_password:

            messages.error(
                request,
                'New passwords do not match.'
            )

            return render(
                request,
                'change_password.html'
            )

        # Minimum password length
        if len(new_password) < 6:

            messages.error(
                request,
                'Password must contain at least 6 characters.'
            )

            return render(
                request,
                'change_password.html'
            )

        # Save password
        student.password = make_password(
            new_password
        )

        student.save()

        # Logout after password change
        request.session.flush()

        return redirect(
            'login'
        )

    return render(
        request,
        'change_password.html'
    )