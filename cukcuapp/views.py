from django.shortcuts import render, redirect
from .models import TeamMember, Book, Leader
from .forms import TeamMemberForm, BookForm


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
    books = Book.objects.order_by('-upload_at')
    return render(request, 'library.html', {'books': books})

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
    leaders = Leader.objects.all()
    return render(request, 'leaderboard.html', {"leaders": leaders})

def team(request):
    executive_members = TeamMember.objects.filter(category='executive')
    ministerial_members = TeamMember.objects.filter(category='ministerial')

    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team')
    else:
        form = TeamMemberForm()

    return render(request, 'team.html', {
        'executive_members': executive_members,
        'ministerial_members': ministerial_members,
        'form': form,
    })













