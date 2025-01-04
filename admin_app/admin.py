from django.contrib import admin
from orders_app.models import Order
from profile_app.models import Profile
from offers_app.models import Offer, OfferDetail
from reviews_app.models import Review


# Proxy-Modelle erstellen
class ProfileProxy(Profile):
    class Meta:
        proxy = True
        app_label = 'admin_app'
        verbose_name = 'Benutzerprofil'
        verbose_name_plural = 'Benutzerprofile'


class OrderProxy(Order):
    class Meta:
        proxy = True
        app_label = 'admin_app'
        verbose_name = 'Bestellung'
        verbose_name_plural = 'Bestellungen'


class OfferProxy(Offer):
    class Meta:
        proxy = True
        app_label = 'admin_app'
        verbose_name = 'Angebot'
        verbose_name_plural = 'Angebote'


class OfferDetailProxy(OfferDetail):
    class Meta:
        proxy = True
        app_label = 'admin_app'
        verbose_name = 'Angebot-Details'
        verbose_name_plural = 'Angebot-Details'


class ReviewProxy(Review):
    class Meta:
        proxy = True
        app_label = 'admin_app'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


# Admin-Klassen
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_user_first_name', 'customer_user_last_name',
                    'business_user_first_name', 'business_user_last_name',
                    'title', 'status', 'offer_type')

    def customer_user_first_name(self, obj):
        return obj.customer_user.first_name
    customer_user_first_name.short_description = 'Vorname (Kunde)'

    def customer_user_last_name(self, obj):
        return obj.customer_user.last_name
    customer_user_last_name.short_description = 'Nachname (Kunde)'

    def business_user_first_name(self, obj):
        return obj.business_user.first_name
    business_user_first_name.short_description = 'Vorname (Geschäft)'

    def business_user_last_name(self, obj):
        return obj.business_user.last_name
    business_user_last_name.short_description = 'Nachname (Geschäft)'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'email', 'type')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'title', 'created_at', 'min_price')

    def user_first_name(self, obj):
        return obj.user.first_name if obj.user else "-"
    user_first_name.short_description = 'Vorname'

    def user_last_name(self, obj):

        return obj.user.last_name if obj.user else "-"
    user_last_name.short_description = 'Nachname'


class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'title', 'offer_type', 'price')

    def user_first_name(self, obj):
        return obj.user.first_name if obj.user else "-"
    user_first_name.short_description = 'Vorname'

    def user_last_name(self, obj):

        return obj.user.last_name if obj.user else "-"
    user_last_name.short_description = 'Nachname'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business_user', 'reviewer',
                    'rating', 'description', 'created_at')


# Registrierung der Proxy-Modelle
admin.site.register(ProfileProxy, ProfileAdmin)
admin.site.register(OrderProxy, OrderAdmin)
admin.site.register(OfferProxy, OfferAdmin)
admin.site.register(ReviewProxy, ReviewAdmin)
admin.site.register(OfferDetailProxy, OfferDetailAdmin)

# Admin-Panel Einstellungen
admin.site.site_header = 'Coderr Verwaltung'
admin.site.site_title = 'Admin-Panel'
admin.site.index_title = 'Willkommen im Coderr Verwaltungsbereich'
