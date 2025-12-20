
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from cukcuapp import views

urlpatterns = [
    path('', views.maintenance, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('choir/', views.choir, name='choir'),
    path('drama/', views.drama, name='drama'),
    path('portfolio/', views.portfolio,name='portfolio'),
    path('starter/', views.starter, name='starter'),
    path('team/', views.team, name='team'),
    path('advocacy/', views.advocacy, name='advocacy'),
    path('bibleStudy/', views.bibleStudy, name='bibleStudy'),
    path('children/', views.children, name='children'),
    path('cream/', views.cream, name='cream'),
    path('decor/', views.decor, name='decor'),
    path('discipleship/', views.discipleship, name='discipleship'),
    path('fridayservice/', views.fridayService, name='fridayservice'),
    path('gentlemen/', views.gentlemen, name='gentlemen'),
    path('hospitality/', views.hospitality, name='hospitality'),
    path('ict/', views.ict, name='ict'),
    path('ladies/', views.ladies, name='ladies'),
    path('library/', views.library, name='library'),
    path('mercy/', views.mercy, name='mercy'),
    path('pw/', views.pw, name='pw'),
    path('prayers/', views.prayers, name='prayers'),
    path('primaryHighschool/', views.primaryHighschool, name='primaryHighschool'),
    path('sundayservice/', views.sundayservice, name='sundayservice'),
    path('worship/', views.worship, name='worship'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('exec', views.exec, name='exec'),
    path("sitemap.xml", TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
