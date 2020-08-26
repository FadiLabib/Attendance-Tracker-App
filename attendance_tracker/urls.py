from django.urls import path
from attendance_tracker.views import SEventsListView, UEventsListView, SEventsDetailView, UEventsDetailView, STakeAttendanceView, UTakeAttendanceView, SEventsCreateView, AssigneesAutoComplete, UEventsCreateView, SEventsUpdateView, UEventsUpdateView, SEventsDeleteView, UEventsDeleteView, SEventsByUserListView, UEventsByUserListView
from django.contrib.auth.decorators import login_required
from attendance_tracker.decorators import user_is_ultimate, user_is_professional, user_is_standard
from attendance_tracker import views

urlpatterns = [
    path('', views.home, name ='attendance-home'),
    path('events/s_<int:pk>/', login_required(user_is_standard(STakeAttendanceView.as_view())), name ='s-take-attendance'),
    path('events/u_<int:pk>/', login_required(user_is_ultimate(UTakeAttendanceView.as_view())), name ='u-take-attendance'),
    path('events/s_create_new/', login_required(user_is_standard(SEventsCreateView.as_view())), name ='s-event-create'),
    path('assignees-autocomplete/', login_required(user_is_ultimate(AssigneesAutoComplete.as_view())), name='assignees-autocomplete'),
    path('events/u_create_new/', login_required(user_is_ultimate(UEventsCreateView.as_view())), name ='u-event-create'),
    path('events/s_<int:pk>/update/', login_required(user_is_standard(SEventsUpdateView.as_view())), name ='s-event-update'),
    path('events/u_<int:pk>/update/', login_required(user_is_ultimate(UEventsUpdateView.as_view())), name ='u-event-update'),
    path('events/', login_required(user_is_standard(SEventsListView.as_view())), name ='s-event-list'), 
    path('u_events/', login_required(user_is_ultimate(UEventsListView.as_view())), name ='u-event-list'),
    path('events/s_<str:email>/', login_required(user_is_standard(SEventsByUserListView.as_view())), name='s-events-by-user'),
    path('events/u_<str:email>/', login_required(user_is_ultimate(UEventsByUserListView.as_view())), name='u-events-by-user'),
    path('events/s_<int:pk>/view/', login_required(user_is_standard(SEventsDetailView.as_view())), name = 's-event-view'),
    path('events/u_<int:pk>/view/', login_required(user_is_ultimate(UEventsDetailView.as_view())), name = 'u-event-view'),
    path('events/s_<int:pk>/delete/', login_required(user_is_standard(SEventsDeleteView.as_view())), name ='s-event-delete'),
     path('events/u_<int:pk>/delete/', login_required(user_is_standard(UEventsDeleteView.as_view())), name ='u-event-delete'),
    path('about/', views.about, name ='attendance-about'),
    path('clslist/', login_required(views.standardclasslist), name ='class-list'),
    path('expclslist/', login_required(user_is_ultimate(views.expandedclasslist)), name='exp-list'),
]