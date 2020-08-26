from django.contrib import admin
from attendance_tracker.models import UserProfile, StudentBasic, StudentGrLevel, StudentCntInf, Counter, Events

admin.site.register(StudentBasic)
admin.site.register(StudentGrLevel)
admin.site.register(StudentCntInf)
admin.site.register(UserProfile)
admin.site.register(Counter)
admin.site.register(Events)