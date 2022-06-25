

from django.urls import path
from . views import *

urlpatterns = [
     path('', home , name='home'),
     path('login/', login_page , name='login'),
     path('register/', register_page , name='register'),
     # path('logout/', 'django.contrib.auth.views.logout', {'next_page': '/login/'}),
     path('logout/', logout_user , name='logout'),
     path('about',about , name='about'),
     path('details/<str:uid>', details , name='details'),

]
