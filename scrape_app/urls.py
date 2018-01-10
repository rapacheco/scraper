from django.conf.urls import url

from scrape_app import views

app_name = 'scrape_app'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.user_login, name='login'),
]
