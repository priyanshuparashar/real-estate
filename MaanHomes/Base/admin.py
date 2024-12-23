from django.contrib import admin

from .models import Profile, Property, PropertyImage, Inquiry, FavoriteProperty, SubscriptionPlan, FeaturedListing, Review, Transaction


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_agent', 'is_owner')
    list_filter = ('is_agent', 'is_owner')
    search_fields = ('user__username', 'phone_number')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'property_type', 'transaction_type',
                    'price', 'location', 'status', 'listed_date')
    list_filter = ('property_type', 'transaction_type',
                   'status', 'location', 'listed_date')
    search_fields = ('title', 'location', 'owner__user__username')
    readonly_fields = ('listed_date',)
    list_editable = ('status',)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    search_fields = ('property__title',)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'contact_info', 'inquiry_date')
    list_filter = ('property', 'inquiry_date')
    search_fields = ('user__username', 'property__title', 'contact_info')


@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'added_on')
    list_filter = ('added_on',)
    search_fields = ('user__username', 'property__title')


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    list_filter = ('price', 'duration_days')
    search_fields = ('name',)


@admin.register(FeaturedListing)
class FeaturedListingAdmin(admin.ModelAdmin):
    list_display = ('property', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('property__title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('user__username', 'property__title')
    readonly_fields = ('review_date',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_date', 'transaction_type')
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('user__username', 'transaction_type')
    readonly_fields = ('transaction_date',)
