from django.contrib import admin
from django.shortcuts import render

from .models import Coach, User, GymMembership, Profile, SubPlan, Schedule


admin.site.register(Coach)
admin.site.register(Profile)
admin.site.register(Schedule)
admin.site.register(SubPlan)
admin.site.register(GymMembership)
