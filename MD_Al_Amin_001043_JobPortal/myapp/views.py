from functools import reduce
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db.models import Q




from django.db.models import Q

def home(request):
    user = request.user
    recommended_jobs = None

    if user.is_authenticated and user.user_type == 'jobseeker':
        jobseeker_profile = jobseekerprofile.objects.get(user=user)


        matching_jobs = addjob_Model.objects.filter(
            reduce(Q.__or__, [Q(required_skills__icontains=skill) for skill in jobseeker_profile.skills.split(',')]),
            ~Q(job_creator=user)
        ).distinct()

        recommended_jobs = matching_jobs

    context = {
        'recommended_jobs': recommended_jobs
    }

    return render(request, "home.html", context)





def signuppage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        display_name=request.POST.get('displayName')
        email=request.POST.get('email')
        password=request.POST.get('password')
        User_type=request.POST.get('userType')
        
        user=Custom_User.objects.create_user(username=username,password=password)
        user.fullname=display_name
        user.email=email
        user.user_type=User_type
        
        user.save()
        
        if user.user_type == 'recruiter':
            user=recruiterprofile.objects.create(user=user)
            user.save()
        else:
            user=jobseekerprofile.objects.create(user=user)
            user.save()
        return redirect('loginpage')
    
    return render(request,'signup.html')

def loginpage(request):
    
    if request.method=='POST':
        myusername=request.POST.get('username')
        mypassword=request.POST.get('password')
        
        user = authenticate(request, username=myusername, password=mypassword)
        print(user)
        
        if user:
            login(request, user)
            return redirect("dashboard")
        
    return render(request,"login.html")

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def viewjobpage(request):
    job=addjob_Model.objects.all()
    context={
        'vjkey':job
    }
    return render(request,"viewjob.html", context)

@login_required
def addjobpage(request):
    user = request.user
   
    if request.method == "POST":
        
        jobtitle=request.POST.get("jobTitle")
        company=request.POST.get("company")
        location=request.POST.get("location")
        description=request.POST.get("description")
        required_skills=request.POST.get("requiredSkills")
        catagory=request.POST.get("category")
        number_of_openings=request.POST.get("openings")
               
        
        job=addjob_Model(
            Job_title=jobtitle,
            Company=company,
            Location=location,
            Description=description,
            required_skills=required_skills,
            catagory=catagory,
            number_of_openings=number_of_openings,
            job_creator = user,
            
        )
        job.save()
        
        return redirect('viewjobpage')
    return render(request, 'Recruiter/addjob.html')

def deletepage(request,myid):
    job=addjob_Model.objects.filter(id=myid)
    job.delete()
    return redirect("viewjobpage")

def editjob(request,myid):
    job=addjob_Model.objects.filter(id=myid)
    
    return render(request, "Recruiter/editjob.html",{'job':job})

def updatepage(request):
    user = request.user
   
    if request.method == "POST":
        
        id=request.POST.get("id")
        jobtitle=request.POST.get("jobTitle")
        company=request.POST.get("company")
        location=request.POST.get("location")
        description=request.POST.get("description")
        catagory=request.POST.get("category")
        number_of_openings=request.POST.get("openings")
               
        
        job=addjob_Model(
            
            id=id,
            Job_title=jobtitle,
            Company=company,
            Location=location,
            Description=description,
            catagory=catagory,
            number_of_openings=number_of_openings,
            job_creator = user,
            
        )
        job.save()
        
        return redirect('viewjobpage')
    
def applypage(request,myid):
    job=get_object_or_404(addjob_Model, id=myid)
    if request.method == 'POST':
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        profile_pic=request.FILES.get('')
        skills = request.POST.get('skills')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        gender = request.POST.get('gender')
        expected_salary=request.POST.get('expected_salary')
        myresume=request.FILES.get('resume')
        if skills and myresume:
            job_seeker=request.user
        
        application=job_apply_model.objects.create(
            job=job,
            applicant=job_seeker,
            email=email,
            phone=phone,
            profile_pic=profile_pic,
            skills=skills,
            present_address=present_address,
            permanent_address=permanent_address,
            gender=gender,
            expected_salary=expected_salary,
            apply_resume=myresume,
        )
        application.save()
        messages.success(request,'Apply Succesfully')
        return redirect('profilepage')
    context={
        'job':job
    }
    return render(request, 'applyjob.html', context)
    
def profilepage(request):
    user = request.user
    applied_jobs = None
    job_posts=None
    
    if user.is_authenticated:
        if user.user_type == 'jobseeker':
            jobseeker_profile = None
            
            jobseeker_profile = jobseekerprofile.objects.get(user=user)
            applied_jobs = job_apply_model.objects.filter(applicant=jobseeker_profile.user)
            
        elif user.user_type == 'recruiter':
            
            recruiter_profile = recruiterprofile.objects.get(user=user)
            job_posts = addjob_Model.objects.filter(job_creator=recruiter_profile.user)
            
            
        else:
            messages.error(request, 'Invalid user type')
            return redirect('loginpage')

        context = {
            'user': user,
            'applied_jobs': applied_jobs,
            'job_posts': job_posts,
            }

        return render(request, "profile.html", context)
    else:
        messages.error(request, 'You need to log in first.')
        return redirect('login')
    
def Applicants_view_page(request, id):
    myjob=get_object_or_404(addjob_Model, id=id)
    job=job_apply_model.objects.filter(job=myjob)
    context={
        'myjob':myjob,
        'job':job,
    }
    return render(request, 'Recruiter/Applicants_view_page.html', context )

    
def see_profile(request, id):
    myjob=get_object_or_404(addjob_Model, id=id)
    job=job_apply_model.objects.filter(job=myjob)
    context={
        'myjob':myjob,
        'job':job,
    }
    return render(request, 'see_profile.html',context)


def editprofilepage(request):
    user = request.user

    if request.method == 'POST':
        userid = request.POST.get('id')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        fullName = request.POST.get('fullName')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        password = request.POST.get('password')


        if not check_password(password, user.password):
            messages.error(request, 'Profile not updated because the password does not match')
            return redirect('profilepage')

        user.id = userid
        user.fname = firstname
        user.lname = lastname
        user.fullname = fullName
        user.phone = phone

        if image:
            user.profile_pic = image

        if user.user_type == 'jobseeker':
            skills = request.POST.get('skills')
            present_address = request.POST.get('present_address')
            permanent_address = request.POST.get('permanent_address')
            gender = request.POST.get('gender')
            resume = request.FILES.get('resume')
            expected_salary=request.POST.get('expected_salary')
            
            
            user.Jobseekerprofile.skills =skills
            user.Jobseekerprofile.present_address = present_address
            user.Jobseekerprofile.permanent_address = permanent_address
            user.Jobseekerprofile.gender=gender
            user.Jobseekerprofile.resume=resume
            user.Jobseekerprofile.expected_salary=expected_salary
            user.Jobseekerprofile.save()

        elif user.user_type == 'recruiter':
            company_name = request.POST.get('companyName')
            recruiter_profile, created = recruiterprofile.objects.get_or_create(user=user)
            recruiter_profile.companyname = company_name
            recruiter_profile.save()

        user.save()
        messages.success(request, 'Profile successfully updated')
        return redirect('profilepage')

    return render(request, 'profile.html')



def changepassword(request):
    user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not check_password(old_password, user.password):
            messages.error(request, 'Current password is wrong')
            # Show error modal
            return render(request, "profile.html", {'show_error_modal': True})

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password did not match')
            # Show error modal
            return render(request, "profile.html", {'show_error_modal': True})

        else:
            user.set_password(confirm_password)
            user.save()
            return redirect("loginpage")

    return render(request, "profile.html")


def searchpage(request):
    try:
        query=request.GET.get('search_query')
        if query:
            jobs=addjob_Model.objects.filter(Job_title__icontains=query)
        else:
            jobs=[]
        context={
            'jobs':jobs,
            'query':query,
        }
        return render(request, 'searchpage.html', context)
    except Exception as e:
        return HttpResponse('Exception error',{{e}})

