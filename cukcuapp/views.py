from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
import cloudinary.uploader
from django.http import JsonResponse
from unicodedata import category

from .forms import ContactForm
from .models import TeamMember, Leader, Book, Exec
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def home_check(request):
    return JsonResponse({"status": "ok", "message": "CUKCU Django app running"})


def healthz(request):
    return HttpResponse("OK", status=200)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')  # redirect to the same page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def portfolio(request):
    return render(request, 'portfolio.html')

def starter(request):
    return render(request, 'starter-page.html')

def exec(request):
    try:

        executive_members = Exec.objects.filter(category='executive')

        context = {
            'executive_members': executive_members,
        }
        return render(request, 'exec.html', context)
    except Exception as e:
        messages.error(request, f"Error loading team page: {str(e)}")
        return render(request, 'error.html', {'error_message': str(e)})


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

# def library(request):
#     try:
#         books = Book.objects.all().order_by('-uploaded_at')
#         return render(request, 'library.html', {'books': books})
#     except Exception as e:
#         messages.error(request, f"Error loading library page: {str(e)}")
#         return render(request, 'library.html', {'books': []})

def library(request):
    try:
        books = Book.objects.all().order_by('-uploaded_at')

        # Debug: Check what's in the database
        print(f"Found {books.count()} books")
        for book in books:
            print(f"Book: {book.title}")
            print(f"PDF File: {book.pdf_file}")
            print(f"PDF URL: {book.get_pdf_url()}")
            print("---")

        return render(request, 'library.html', {'books': books})
    except Exception as e:
        messages.error(request, f"Error loading library page: {str(e)}")
        print(f"Library error: {e}")
        return render(request, 'library.html', {'books': []})



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
        return render(request, 'leaderboard.html', {"leaders": leaders})
    except Exception as e:
        messages.error(request, f"Error loading leaderboard page: {str(e)}")
        return render(request, 'error.html', {'error_message': str(e)})


def team(request):
    try:
        focus_members = TeamMember.objects.filter(category='focus')
        executive_members = TeamMember.objects.filter(category='executive')
        ministerial_members = TeamMember.objects.filter(category='ministerial')

        context = {
            'focus_members': focus_members,
            'executive_members': executive_members,
            'ministerial_members': ministerial_members,
        }
        return render(request, 'team.html', context)
    except Exception as e:
        messages.error(request, f"Error loading team page: {str(e)}")
        return render(request, 'error.html', {'error_message': str(e)})


def debug_upload(request):
    """Debug view to test Cloudinary upload directly"""
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']

            # Test direct upload to Cloudinary
            result = cloudinary.uploader.upload(
                file,
                resource_type='raw',
                folder='books',
                use_filename=True,
                unique_filename=True,
                overwrite=False
            )

            return JsonResponse({
                'status': 'success',
                'result': result,
                'public_id': result['public_id'],
                'secure_url': result['secure_url'],
                'resource_type': result['resource_type']
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e),
                'error_type': type(e).__name__
            })

    return JsonResponse({'message': 'Send a POST request with a file'})


def coming_soon(request):
    """
    Display the Coming Soon page with countdown timer.
    """
    # Pass the launch datetime from settings
    launch_datetime = settings.COMING_SOON_LAUNCH_DATETIME
    context = {
        "launch_datetime": launch_datetime,
    }
    return render(request, "coming_soon.html", context)

def maintenance(request):
    return render(request, "maintenance.html")






