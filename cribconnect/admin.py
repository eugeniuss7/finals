from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

from cribconnect.models import account

class accountInLine(admin.StackedInline):
    model = account
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [accountInLine]

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(account)
admin.site.register(listing)
admin.site.register(inquiryRequest)
admin.site.register(cribshare)
admin.site.register(rateReviews)
admin.site.register(listingAddress)
admin.site.register(listingFeatures)
admin.site.register(paymentTerms)
admin.site.register(imageGallery)