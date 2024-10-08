from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .forms import EmployerJobCreationForm, EmployerProfileForm
from .models import Company, JobRequests


def is_employer(user):
    try:
        if user.is_jobseeker:
            raise Http404
        return True
    except:
        raise Http404


@user_passes_test(is_employer)
@login_required
def employer_home(request):
    """
    show list of requests by jobseekers on jobs created by employer
    ------------------
    when user logged in for first ever; right after the registeration
    the exception happens because user/employer has not profile yet.
    in this case we redirect user to employer_profile() to make the profile.
    """     
    try:
        requests = JobRequests.objects.filter(
            employer=request.user.company, accepted=False
            ).all()
        accepted_requests = JobRequests.objects.filter(
            employer=request.user.company, accepted=True
            ).all()
    except Company.DoesNotExist:
        messages.success(
            request,
            'برای دسترسی به بخش های دیگر ابتدا اطلاعات زیر را تکمیل کنید'
        )
        return redirect('employer-profile')
    context = {
        'requests':requests,
        'accepted_requests': accepted_requests,
        }
    return render(request, 'employer_home.html', context)


@user_passes_test(is_employer)
@login_required
def employer_profile(request):
    """ 
    Company Profile
    request.user = employer
    -----------------------
    when a user registered and logged in for first ever time;
    to let the employer create a job we need their information.
    so step-1 is to complete their profile - actually we create a company profile.
    that case handles in the exception;
    when the "RelatedObject.DoesNotExist" error appears.
    otherwise when employer already has a profile, form shows the information
    from database and employer can update their informations.
    """
    try: # if user already has a profile show their information in form 
        if request.method == 'POST':
            form = EmployerProfileForm(
                request.POST, request.FILES, instance=request.user.company
                )
            if form.is_valid():
                instance = form.save(commit=False)
                instance.employer = request.user
                instance.save()
                messages.success(request, 'ستاسو پروفایل اپدیت شو')
                return redirect('employer-profile')
        form = EmployerProfileForm(instance=request.user.company)
    except Company.DoesNotExist: 
            # if user is new and has not a profile
            if request.method == 'POST':
                form = EmployerProfileForm(request.POST)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.employer = request.user
                    instance.save()
                    messages.success(request, 'ستاسو پروفایل جوړ شو')
                    messages.success(
                        request,
                        """
                        د پورته مینو اختیار څخه د اعلان جوړولو لپاره
                        نوی اعلان غوره کړئ
                        """
                    )
                    return redirect('employer-profile')
            form = EmployerProfileForm()
    return render(request, 'profile.html', {'form':form})


@user_passes_test(is_employer)
@login_required
def employer_jobs(request):
    """ show all jobs published by the employer/company."""
    try:
        jobs = request.user.company.jobs.all()
        now = datetime.now(timezone.utc)
        for i in jobs:
            get_days = now - i.created_date
            if get_days.days > 1:
                i.created_date = f'{get_days.days} ورځی مخکی' 
        requests = JobRequests.objects.filter(employer=request.user.company)
    except Company.DoesNotExist:
        return redirect('employer-home')
    return render(request, 'jobs.html', {'jobs':jobs, 'number':len(requests)})


@user_passes_test(is_employer)
@login_required
def employer_create_job(request):
    """ create a job and publishe it to the portal"""
    try:
        if request.method == 'POST':
            form = EmployerJobCreationForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = request.user.company
                instance.save()
                messages.success(request, 'ستاسو اعلان نشر شو')
                return redirect('job-detail', id=instance.id)
        elif request.method == 'GET':
            form = EmployerJobCreationForm()
    except Company.DoesNotExist:
        raise Http404
    return render(request, 'create_job.html', {'form':form})


def accepted_status(request, id):
    req = JobRequests.objects.filter(id=id).first()
    req.accepted = True
    req.save()
    # also update the accepted status in jobseeker requests table
    jobseeker_request = req.jobseeker.requests.filter(id=id).first()
    jobseeker_request.status = 'تایید شوی'
    jobseeker_request.save()
    return redirect('employer-home')


def hired_status(request, id):
    req = JobRequests.objects.filter(id=id).first()
    req.hired = True
    return redirect('employer-home')


def delete_request(request, id):
    req = JobRequests.objects.filter(id=id).delete()
    return redirect('employer-home')