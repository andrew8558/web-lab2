from django.urls import path, include
import hw_board.views

urlpatterns = [
    path('', hw_board.views.main, name="main"),
    path('login/', hw_board.views.login_view, name="login"),
    path('signup/', hw_board.views.signup, name="signup"),
    path('courses/<str:course_name>/', hw_board.views.course, name="course"),
    path('homework/<int:hw_id>/', hw_board.views.homework, name="homework"),
    path('profile/', hw_board.views.profile, name="profile"),
    path('journal/', hw_board.views.journal, name='journal')
]
