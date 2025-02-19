from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('edit/', views.edit_profile, name='edit_profile'),
    # other URL patterns...
    path('group_discussions/', views.group_discussions, name='group_discussions'),
    path('documents/', views.documents, name='documents'),
    path('join_group/<int:group_id>/', views.join_group, name='join_group'),
    path('resource/<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('add_task/', views.add_task, name='add_task'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('search_results/', views.search_results, name='search_results'),
    path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),

]
