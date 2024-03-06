from django.contrib import admin
from myapp.models import *
# Register your models here.


class Custom_User_Display(admin.ModelAdmin):
    list_display=[ 'username','fullname','email','user_type' ]

class addjob_Model_Display(admin.ModelAdmin):
    list_display=[ 'Job_title','Company','Location' ]
    
class addjob_Model_Display(admin.ModelAdmin):
    list_display=[ 'Job_title','Company','Location' ]
    
  
    
    
    
admin.site.register(Custom_User,Custom_User_Display)
admin.site.register(addjob_Model,addjob_Model_Display)
admin.site.register(recruiterprofile)
admin.site.register(jobseekerprofile)
admin.site.register(job_apply_model)
