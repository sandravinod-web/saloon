from django.contrib import admin
from .models import User, Client, Branch, Service, Staff, Customer, Appointment

# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)

admin.site.register(User, UserAdmin)

# Client Admin
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'business_type', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('business_type',)

admin.site.register(Client, ClientAdmin)

# Branch Admin
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'client', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('client',)

admin.site.register(Branch, BranchAdmin)

# Service Admin
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'price', 'duration', 'created_at')
    search_fields = ('name',)
    list_filter = ('branch',)

admin.site.register(Service, ServiceAdmin)

# Staff Admin
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'email', 'phone', 'role', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('branch',)

admin.site.register(Staff, StaffAdmin)

# Customer Admin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('branch',)

admin.site.register(Customer, CustomerAdmin)

# Appointment Admin
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'branch', 'customer', 'staff', 'service', 'created_at')
    search_fields = ('customer__name', 'branch__name', 'staff__name', 'service__name')
    list_filter = ('branch', 'date', 'staff')

admin.site.register(Appointment, AppointmentAdmin)
