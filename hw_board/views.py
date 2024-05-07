from django.shortcuts import render
from .models import Student, Course, HomeworkType, HwDone
from django.urls import path
from .forms import SubmitAnswer, LoginForm, SignUpForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    logout(request)

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            tmp_user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            if tmp_user is not None:
                login(request, tmp_user)
                return HttpResponseRedirect('/hw_board/')

    context = {
        'form': form,
    }
    return render(request, 'hw_board/login_form.html', context)


def signup(request):

    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['name'],
                last_name=form.cleaned_data['surname'],
                email=form.cleaned_data['email']
            )
            new_user.save()
            new_student = Student(name=new_user.first_name, surname=new_user.last_name, email=new_user.email, password=new_user.password)
            new_student.save()
            return HttpResponseRedirect('/hw_board/login/')

    context = {
        'form': form,
    }
    return render(request, 'hw_board/signup_form.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/hw_board/login/')

    courses = Course.objects.all()

    context = {
        'name': request.user.first_name,
        'surname': request.user.last_name,
        'email': request.user.email,
        'courses': courses,
    }
    return render(request, 'hw_board/profile.html', context)


def course(request, course_name):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/hw_board/login/')

    courses = Course.objects.all()
    course = courses.get(name=course_name)

    student = Student.objects.all().get(email=request.user.email)

    duty_list = HomeworkType.objects.all().filter(course=course.id)
    done_list = HwDone.objects.all().filter(student=student)
    stat = []

    for hw_type in duty_list:
        mark = 0
        try:
            hw_dones = done_list.filter(hw_type=hw_type)
            hw_done = hw_dones[len(hw_dones)-1]
            mark = hw_done.mark
        except:
            pass
        finally:
            stat.append([hw_type, mark])

    context = {
        "course_name": course.name,
        "duty_list": duty_list,
        'courses': courses,
        'stat': stat
    }
    return render(request, 'hw_board/course.html', context)


def homework(request, hw_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/hw_board/login/')

    hw = HomeworkType.objects.all().get(pk=hw_id)
    form = SubmitAnswer()

    if request.method == 'POST':
        form = SubmitAnswer(request.POST)
        if form.is_valid():
            student = Student.objects.all().get(email=request.user.email)
            new_hw = HwDone(text=form.cleaned_data['content'], student=student, mark=0, hw_type=hw)
            new_hw.save()
            return HttpResponseRedirect(f'/hw_board/homework/{hw_id}/')

    courses = Course.objects.all()

    context = {
        "task": hw.task,
        "deadline": hw.deadline,
        'courses': courses,
        'form': form,
        'hw_id': hw_id
    }

    return render(request, 'hw_board/hw.html', context)


def main(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/hw_board/login/')

    courses = Course.objects.all()

    context = {
        'courses': courses,
    }

    return render(request, 'hw_board/main.html', context)


def journal(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/hw_board/login/')
    
    courses = Course.objects.all()
    students = Student.objects.all()
    hw_types = HomeworkType.objects.all()
    hw_dones = HwDone.objects.all()
    stat = []

    for student in students:
        hw_dones_tmp = hw_dones.filter(student=student)
        if not hw_dones_tmp:
            continue
        for hw_type in hw_types:
            mark = 0
            hw_done_best = None
            for hw_done in hw_dones_tmp:
                if hw_done.hw_type.name == hw_type.name and hw_done.mark >= mark:
                    hw_done_best = hw_done
                    mark = hw_done.mark
            if hw_done_best:
                stat.append([student, hw_type, mark])

    context = {
        'courses': courses,
        'stat': stat
    }

    return render(request, 'hw_board/journal.html', context)
