from django.shortcuts import render, get_object_or_404
from .models import PendingUser, Task
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from .models import Task, User,Comment
from .forms import CommentForm, TaskForm, LoginForm, FinalSubmissionForm


def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, get_object_or_404
from .models import Task


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=user)

    grouped_tasks = {
        'PENDING': tasks.filter(status='PENDING'),
        'IN_PROGRESS': tasks.filter(status='IN_PROGRESS'),
        'COMPLETED': tasks.filter(status='COMPLETED'),
    }
    return render(request, 'core/dashboard.html', {'grouped_tasks': grouped_tasks, 'now': timezone.now()})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'core/dashboard.html', {'tasks': tasks})


@staff_member_required

def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to_id = request.POST['assigned_to']
        deadline = request.POST['deadline']

        Task.objects.create(
            title=title,
            description=description,
            assigned_to=User.objects.get(id=assigned_to_id),
            deadline=deadline,
            final_description=""  # This avoids IntegrityError
        )
        return redirect('dashboard')  # or wherever you go next
    else:
        users = User.objects.all()
        return render(request, 'core/create_task.html', {'users': users})
    return render(request, 'create_task.html', {'form': form})

@login_required
def add_comment(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user  # ✅ This is the missing line
            comment.save()
            return redirect('dashboard')

    else:
        form = CommentForm()
    return render(request, 'core/add_comment.html', {'form': form})


@login_required
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
    return redirect('dashboard')


@login_required
def submit_for_review(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.assigned_to or task.status != 'COMPLETED':
        return redirect('dashboard')

    if request.method == 'POST':
        form = FinalSubmissionForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.submitted_for_review = True
            task.save()
            return redirect('dashboard')
    else:
        form = FinalSubmissionForm(instance=task)

    return render(request, 'core/submit_review.html', {'form': form, 'task': task})


@login_required
def submitted_tasks(request):
    if not request.user.is_staff:
        return redirect('dashboard')
        
    tasks = Task.objects.filter(submitted_for_review=True)
    return render(request, 'core/submitted_tasks.html', {'tasks': tasks})



@login_required
def review_task(request, task_id):
    if not request.user.is_staff:
        return redirect('dashboard')

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        decision = request.POST.get('decision')
        feedback = request.POST.get('final_description', '').strip()

        task.final_description = feedback

        if decision == 'accept':
            task.status = 'VERIFIED'
            task.review_status = 'VERIFIED'
            task.submitted_for_review = False
            messages.success(request, f"Task '{task.title}' has been verified successfully.")
        elif decision == 'reject':
            task.status = 'IN_PROGRESS'
            task.review_status = 'REJECTED'
            task.submitted_for_review = False
            messages.warning(request, f"Task '{task.title}' has been rejected. User will revise it.")

        task.save()
        return redirect('submitted_tasks')

    return render(request, 'core/review_task.html', {'task': task})



@staff_member_required
def pending_users(request):
    users = PendingUser.objects.all()
    return render(request, "core/pending_users.html", {"pending_users": users})


@staff_member_required
def approve_user(request, user_id):
    pending = PendingUser.objects.get(id=user_id)
    User.objects.create_user(username=pending.username, email=pending.email, password=pending.password)
    pending.delete()
    messages.success(request, f"User '{pending.username}' approved.")
    return redirect("pending_users")


@staff_member_required
def reject_user(request, user_id):
    pending = PendingUser.objects.get(id=user_id)
    pending.delete()
    messages.info(request, f"User '{pending.username}' rejected.")
    return redirect("pending_users")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "core/signup.html")

        if PendingUser.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "core/signup.html")

        if PendingUser.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, "core/signup.html")

        # Save to pending list
        PendingUser.objects.create(username=username, email=email, password=password)

        messages.success(request, "Account request sent. Waiting for admin approval.")
        return redirect("login")

    return render(request, "core/signup.html")