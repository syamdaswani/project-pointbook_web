from django.contrib import admin

from .models import Partner, PB_Service, Account, PB_Professional, Service_Bridge, PB_Category, PB_Booking

class PartnerAdmin(admin.ModelAdmin):
	list_display = ('user_key', 'name')

class ServiceAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

class AccountAdmin(admin.ModelAdmin):
	list_display = ('user',)

class ProfessionalAdmin(admin.ModelAdmin):
	list_display = ('id', 'first_name', 'last_name')

class ServiceBridgeAdmin(admin.ModelAdmin):
	list_display = ('id', 'partner_name', 'service_name')

	def partner_name(self, instance):
		return instance.partner.name
	def service_name(self, instance):
		return instance.service.name

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)

class BookingAdmin(admin.ModelAdmin):
	list_display = ('user_name',)


admin.site.register(PB_Booking, BookingAdmin)
admin.site.register(PB_Category, CategoryAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(PB_Professional, ProfessionalAdmin)
admin.site.register(PB_Service, ServiceAdmin)
admin.site.register(Service_Bridge, ServiceBridgeAdmin)
admin.site.register(Account, AccountAdmin)