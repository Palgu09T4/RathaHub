from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
# views.py (Optional if you're just wiring URLs)
from django.contrib.auth import views as auth_views

app_name="account"

urlpatterns =[
    path('signup',views.signup,name='signup'),
    path('login',views.loginView,name='login'),
    path('logout',views.logoutView,name='logout'),
    path('profile',views.profileView,name='profile'),
    path('edit',views.editView,name='edit'),
    path('password_reset/', auth_views.password_reset, {
        'template_name': 'account/password_reset_form.html',
        'email_template_name': 'account/password_reset_email.html',
        'subject_template_name': 'account/password_reset_subject.txt',
        'post_reset_redirect': 'account:password_reset_done',  # 👈 This is critical
    }, name='password_reset'),

    path('password_reset/done/', auth_views.password_reset_done, {
        'template_name': 'account/password_reset_done.html'
    }, name='password_reset_done'),

    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, {
        'template_name': 'account/password_reset_confirm.html',
        'post_reset_redirect': 'account:password_reset_complete',  # Optional for confirm
    }, name='password_reset_confirm'),

    path('reset/done/', auth_views.password_reset_complete, {
        'template_name': 'account/password_reset_complete.html'
    }, name='password_reset_complete'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)