from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UpdateProfileForm, UpdateUserForm
from .models import Profile, Coach,Schedule
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import JsonResponse
from .models import GymMembership, SubPlan
from django.db.models import Count



def home(request):
    return render(request, 'main/index.html')


def coach(request):
    coaches = Coach.objects.all()[:10]
    tren = Coach.objects.all()[:10]

    context = {"coaches": coaches, "tren": tren}
    return render(request, 'main/trainers.html', context)


def price_view(request):
    return render(request, 'main/price.html')

def schedule_view(request):
    schedules = Schedule.objects.all()
    return render(request, 'main/schedule.html', {'schedules': schedules})


def register(request):
    if request.method == "POST":
        username = request.POST.get('login')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.info(request, "Пароли не совпадают")
            return redirect('/register')

        try:
            if User.objects.get(username=username):
                messages.warning(request, "Логин занят")
                return redirect('/register')

        except Exception as identifier:
            pass

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Пользователь создан")
        return redirect('/login')

    return render(request, "main/register.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=username, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Вы успешно вошли")
            return redirect('/')
        else:
            messages.error(request, "Неправильные данные")
            return redirect('/login')

    return render(request, "main/login.html")


def handlelogout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли")
    return redirect('/')


def profile(request):
    username = request.user
    posts = User.objects.filter(username=username)
    profile = Profile.objects.filter(user=username)
    context = {'posts': posts, 'profile': profile}
    return render(request, 'main/profile.html', context)


@login_required()
def update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('/profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'main/update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



def update_profile(request):
    if request.method == 'POST':
        selected_membership_id = request.POST.get('membership')
        selected_plan_id = request.POST.get('plan')

        # Получите объект выбранного членства и плана
        selected_membership = GymMembership.objects.get(pk=selected_membership_id)
        selected_plan = SubPlan.objects.get(pk=selected_plan_id)

        # Обновите профиль пользователя
        request.user.profile.selected_membership = selected_membership
        request.user.profile.selected_plan = selected_plan
        request.user.profile.save()

    return redirect('profile')

def membership_view(request):
    if request.user.is_authenticated:
        memberships = GymMembership.objects.all()
        plans = SubPlan.objects.all()
        context = {
            'memberships': memberships,
            'plans': plans,
        }
        if request.method == 'POST':
            selected_membership_id = request.POST.get('membership', None)
            selected_plan_id = request.POST.get('plan', None)
            if selected_membership_id and selected_plan_id:
                selected_membership = GymMembership.objects.get(pk=selected_membership_id)
                selected_plan = SubPlan.objects.get(pk=selected_plan_id)
                # Создаем или обновляем профиль пользователя с информацией о выбранном членстве и плане
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.selected_membership = selected_membership
                profile.selected_plan = selected_plan
                profile.save()
                messages.success(request, f'Абонемент "{selected_membership.name}" и план членства выбраны успешно!')
                return redirect('/profile')
            else:
                messages.error(request, 'Не удалось выбрать абонемент или план. Пожалуйста, попробуйте еще раз.')
        return render(request, 'main/card.html', context)
    else:
        return redirect('/login')

def team_members(request):
    coaches = Coach.objects.all()
    return render(request, 'index.html', {'coaches': coaches})


def stat(request):
    # Получение всех профилей
    profiles = Profile.objects.all()
    # Сбор уникальных членств и их подсчет в профилях
    membership_counts = {}
    for profile in profiles:
        membership_name = profile.selected_membership.name if profile.selected_membership else 'Нет членства'
        membership_counts[membership_name] = membership_counts.get(membership_name, 0) + 1
    # Сбор уникальных длительностей абонемента и их подсчет в профилях
    plan_counts = {}
    for profile in profiles:
        plan_months = profile.selected_plan.months if profile.selected_plan else 'Нет членства'
        plan_counts[plan_months] = plan_counts.get(plan_months, 0) + 1
    # Разделение данных для передачи в шаблон
    labels_membership = list(membership_counts.keys())
    data_membership = list(membership_counts.values())

    labels_plan = list(plan_counts.keys())
    data_plan = list(plan_counts.values())
    context = {
        'labels_membership': labels_membership,
        'data_membership': data_membership,
        'labels_plan': labels_plan,
        'data_plan': data_plan,
    }
    return render(request, 'main/stat.html', context)
