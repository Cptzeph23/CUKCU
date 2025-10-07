from django.shortcuts import render, redirect
from .models import TeamMember, Leader, Book
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def healthz(request):
    return JsonResponse({"status": "ok"})

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def starter(request):
    return render(request, 'starter-page.html')


def advocacy(request):
    return render(request, 'advocacy.html')

def bibleStudy(request):
    return render(request, 'bibleStudy.html')

def children(request):
    return render(request, 'children.html')

def choir(request):
    return render(request, 'choir.html')

def cream(request):
    return render(request, 'cream.html')

def decor(request):
    return render(request, 'decor.html')

def discipleship(request):
    return render(request, 'discipleship.html')

def drama(request):
    return render(request, 'drama.html')

def fridayService(request):
    return render(request, 'fridayservice.html')

def gentlemen(request):
    return render(request, 'gentlemen.html')

def hospitality(request):
    return render(request, 'hospitality.html')

def ict(request):
    return render(request, 'ict.html')

def ladies(request):
    return render(request, 'ladies.html')

def library(request):
    try:
        books = Book.objects.order_by('-upload_at')
        return render(request, 'library.html', {'books': books})
    except Exception as e:
        messages.error(request, f"Error loading library page: {str(e)}")
        return render(request, 'error.html', {'error_message': str(e)})

def mercy(request):
    return render(request, 'mercy.html')

def pw(request):
    return render(request, 'p&w.html')

def prayers(request):
    return render(request, 'prayers.html')

def primaryHighschool(request):
    return render(request, 'primaryHighschool.html')

def sundayservice(request):
    return render(request, 'sundayservice.html')

def worship(request):
    return render(request, 'worship.html')


def leaderboard(request):
    try:
        leaders = Leader.objects.all()
        # Fix image paths
        for leader in leaders:
            if leader.image and not leader.image.startswith('/'):
                leader.image = f"/media/{leader.image}"
        return render(request, 'leaderboard.html', {"leaders": leaders})
    except Exception as e:
        messages.error(request, f"Error loading leaderboard page: {str(e)}")
        return render(request, 'error.html', {'error_message': str(e)})

def team(request):
    try:
        executive_members = TeamMember.objects.filter(category='executive')
        ministerial_members = TeamMember.objects.filter(category='ministerial')
        
        # Ensure image paths are correct
        for member in list(executive_members) + list(ministerial_members):
            if member.image and not member.image.startswith('/'):
                member.image = f"/media/{member.image}"
        
        context = {
            'executive_members': executive_members,
            'ministerial_members': ministerial_members,
        }
        
        return render(request, 'team.html', context)
    except Exception as e:
        messages.error(request, f"Error loading team page: {str(e)}")
        return render(request, 'error.html', {'error_message': str(e)})













