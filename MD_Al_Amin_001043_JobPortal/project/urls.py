from django.contrib import admin
from django.urls import path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home, name="home" ),
    path('',signuppage, name='signuppage'),
    path('loginpage/',loginpage, name='loginpage'),
    path('logoutpage/',logoutpage, name='logoutpage'),
    path('dashboard/',dashboard, name='dashboard'),
    path('viewjobpage/',viewjobpage, name='viewjobpage'),
    path('addjobpage/',addjobpage, name='addjobpage'),
    path('deletepage/<str:myid>',deletepage, name='deletepage'),
    path('editjob/<str:myid>',editjob, name='editjob'),
    path('updatepage/',updatepage, name='updatepage'),
    path('applypage/<str:myid>',applypage, name='applypage'),
    path('profilepage/',profilepage, name='profilepage'),
    path('editprofilepage/',editprofilepage, name='editprofilepage'),
    path('changepassword/',changepassword, name='changepassword'),
    path('searchpage/',searchpage, name='searchpage'),
    path('Applicants_view_page/<str:id>',Applicants_view_page, name='Applicants_view_page'),
    path('see_profile/<str:id>/', see_profile, name='see_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
