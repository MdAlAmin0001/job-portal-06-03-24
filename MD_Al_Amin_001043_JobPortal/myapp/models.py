from django.db import models
from django.contrib.auth.models import AbstractUser



class Custom_User(AbstractUser):
    USER=[
        ('recruiter','Recruiter'),('jobseeker','Jobseeker')
    ]
    
    
    fname=models.CharField(max_length=100, null=True)
    lname=models.CharField(max_length=100, null=True)
    fullname=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    user_type=models.CharField(choices=USER, max_length=120)
    profile_pic=models.ImageField(upload_to='media/profile_pic', null=True)
    phone=models.CharField(max_length=11, null=True)
    
 
class addjob_Model(models.Model):
    Job_title=models.CharField(max_length=100, null=True)
    Company=models.CharField(max_length=100, null= True)
    catagory_choices=[
        ('FULL-TIME','Full-Time'),
        ('PART-Time','Part-Time'),
    ]
    catagory=models.CharField(max_length=255, choices=catagory_choices, null=True, blank=True)
    number_of_openings= models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Expected Salary")
    Skill_choices=[
        ('PYTHON','Python'),
        ('JAVA','Java'),
        ('PHP','php'),
    ]
    required_skills = models.CharField(max_length=255, choices=Skill_choices, null=True, blank=True)
    Location=models.CharField(max_length=100, null= True)
    Description=models.TextField(max_length=100, null=True) 
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    job_creator = models.ForeignKey(Custom_User, on_delete=models.CASCADE, null=True)
    
    
    def __str__(self):
        return self.Job_title   
    
    
class recruiterprofile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE, null=True,related_name='Recruiterprofile')
    companyname=models.CharField(max_length=11, null=True)
    
    
    
    def __str__(self):
        return self.user.fullname
    
    

 
class jobseekerprofile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE, null=True, related_name='Jobseekerprofile')
    Skill_choices=[
        ('PYTHON','Python'),
        ('JAVA','Java'),
        ('PHP','php'),
    ]
    skills=models.CharField(max_length=100, choices=Skill_choices, null=True, blank=True)
    
    present_address=models.CharField(max_length=100, null=True)
    permanent_address=models.CharField(max_length=100, null=True)
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES,)
    resume = models.FileField(upload_to='media/resumes', blank=True, null=True, help_text="Upload Resume (PDF, DOC, DOCX)")
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Expected Salary")

    
    def __str__(self):
       return self.user.fullname
   
   
   
class job_apply_model(models.Model):
    job= models.ForeignKey(addjob_Model, on_delete=models.CASCADE, null=True)
    applicant=models.ForeignKey(Custom_User, on_delete=models.CASCADE, null=True)
    email=models.EmailField(unique=False)
    phone=models.CharField(max_length=11, null=True)
    profile_pic=models.ImageField(upload_to='media/profile_pic', null=True)
    skills=models.CharField(max_length=100, null=True)
    present_address=models.CharField(max_length=100, null=True)
    permanent_address=models.CharField(max_length=100, null=True)
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(max_length=50,choices=GENDER_CHOICES,)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Expected Salary")
    apply_resume=models.FileField(upload_to='media/apply_resume', null=True)
    
    
    def __str__(self):
        return self.applicant.fullname +' Applied for ' +self.job.Job_title
    
    