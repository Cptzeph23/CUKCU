from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TeamMember, Leader

def team_view(request):
    team_members = TeamMember.objects.all()
    return render(request, 'team.html', {'team_members': team_members})

def leaders_view(request):
    leaders = Leader.objects.all()
    return render(request, 'leaders.html', {'leaders': leaders})

@login_required
def admin_dashboard(request):
    team_members = TeamMember.objects.all()
    leaders = Leader.objects.all()
    return render(request, 'admin/dashboard.html', {
        'team_members': team_members,
        'leaders': leaders
    })