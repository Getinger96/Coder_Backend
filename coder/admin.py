from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import Profile, Offer, OfferDetail, Order, Review


# Register your models here.

admin.site.register(Profile)
admin.site.register(Offer)
admin.site.register(OfferDetail)
admin.site.register(Order)
admin.site.register(Review)
