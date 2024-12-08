from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Group, Resource, Event
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import Task

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('task')  # Get the task title from the form
        if title:
            Task.objects.create(user=request.user, title=title)
    return redirect('dashboard')  # Redirect back to the dashboard
from .forms import UserForm, UserProfileForm
from .models import UserProfile


# Create your views here.


def index(request):
    return render(request,'index.html')

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')  # Redirect to the index page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')  # Render the login template
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate password and confirm password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect to login page after successful signup
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect('signup')

    return render(request, 'signup.html')  # Render the signup template

def dashboard(request):
    return render(request,'dashboard.html')
def aboutus(request):
    return render(request,'aboutus.html')


@login_required
def edit_profile(request):
    # Ensure the UserProfile exists
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=user_profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('index')  # Or wherever you want to redirect after updating

    return render(request, 'userprofile/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
from django.contrib.auth import logout  # Import logout

# Logout view
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('index')  # Redirect to index or any page you prefer after logout


# Dashboard view
@login_required
def dashboard(request):
    # Fetch some example data for the dashboard
    groups = Group.objects.all()[:3]  # Limit to 3 for display
    resources = Resource.objects.all()[:3]  # Limit to 3 for display
    events = Event.objects.all()[:3]  # Limit to 3 for display

    return render(request, 'dashboard.html', {
        'groups': groups,
        'resources': resources,
        'events': events
    })


# Group discussion page view
@login_required
def group_discussions(request):
    groups = Group.objects.all()
    return render(request, 'userprofile/group_discussions.html', {'groups': groups})


# Document collaboration view placeholder
@login_required
def documents(request):
    return render(request, 'userprofile/documents.html')  # Template for documents collaboration


# Group join view
@login_required
def join_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'userprofile/group_detail.html', {'group': group})


# Resource detail view
@login_required
def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    return render(request, 'userprofile/resource_detail.html', {'resource': resource})




@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('task')  # Get the task title from the form
        if title:
            Task.objects.create(user=request.user, title=title)
    return redirect('dashboard')  # Redirect back to the dashboard



@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)  # Filter tasks for the logged-in user
    return render(request, 'dashboard.html', {'tasks': tasks})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FeedbackForm
from .models import Feedback

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('dashboard')
    else:
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})

from django.shortcuts import render
from .models import Group, Resource, Event, Task

def search_results(request):
    query = request.GET.get('query', '')  # Get the search query from the GET request
    groups = Group.objects.filter(name__icontains=query)  # Search for groups
    resources = Resource.objects.filter(title__icontains=query)  # Search for resources
    events = Event.objects.filter(title__icontains=query)  # Search for events
    tasks = Task.objects.filter(title__icontains=query)  # Search for tasks

    # Pass the search results to the template
    return render(request, 'userprofile/search_results.html', {
        'query': query,
        'groups': groups,
        'resources': resources,
        'events': events,
        'tasks': tasks,
    })



from django.shortcuts import render
from .models import Notification

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': user_notifications})

def dashboard_view(request):
    notifications = Notification.objects.all()  # Example of fetching notifications from a model
    return render(request, 'dashboard.html', {'notifications': notifications})




# views.py
from django.http import JsonResponse
from .models import Notification

def mark_as_read(request, notification_id):
    if request.method == 'POST' and request.is_ajax():
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True  # Mark the notification as read
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Notification not found'})


'''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Discussion
from .forms import DiscussionForm'''

'''@login_required
def group_discussions(request):
    discussions = Discussion.objects.all().order_by('-created_at')
    return render(request, 'userprofile/group_discussions.html', {'discussions': discussions})

@login_required
def create_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.creator = request.user
            discussion.save()
            return redirect('group_discussions')
    else:
        form = DiscussionForm()
    return render(request, 'create_discussion.html', {'form': form})

@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    return render(request, 'discussion_detail.html', {'discussion': discussion})'''