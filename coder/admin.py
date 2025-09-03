from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import Profile, Offer, OfferDetail, Order, Review


# Register your models here.
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer', 'price')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'first_name', 'last_name', 'location', 'tel')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('offer_detail', 'customer_user', 'status', 'created_at')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business_user', 'reviewer', 'rating', 'created_at')
    
   

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Offer)
admin.site.register(OfferDetail, OfferDetailAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
