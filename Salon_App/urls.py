from django.urls import path
from . import views


urlpatterns = [
    #Login Urls
    path('', views.login, name='login'),

    # Super Admin Dashboard Urls 
    path('super_admin_signup/', views.super_admin_signup, name='super_admin_signup'),
    path('super_admin_login/', views.super_admin_login, name='super_admin_login'),
    path('super-admin-profile/', views.super_admin_profile, name='view_super_admin_profile'),
    path('super-admin-profile/edit/', views.edit_super_admin_profile, name='edit_super_admin_profile'),
    path('super-admin-profile/delete/', views.delete_super_admin_profile, name='delete_super_admin_profile'),
    path('super-admin/clients/', views.view_clients, name='view_clients'),

    # Client Dashboard Urls
    path('client_signup/', views.client_signup, name='client_signup'),
    path('client/profile/', views.view_profile, name='view_profile'),
    path('client/profile/edit/', views.edit_profile, name='edit_profile'),
    path('client/profile/delete/', views.delete_profile, name='delete_profile'),
       
    #Branch Urls(Client Dashboard)
    path('client/add-branch/', views.add_branch, name='add_branch'),
    path('client/branches/', views.view_branches, name='view_branches'),
    path('client/branches/update/<int:branch_id>/', views.update_branch, name='update_branch'),
    path('client/branches/delete/<int:branch_id>/', views.delete_branch, name='delete_branch'),

    #Staff Urls(Client & Branch Dashboard)
    path('add-staff/', views.add_staff, name='add_staff'),
    path('view-staff/', views.view_staff, name='view_staff'),
    path('update-staff/<int:staff_id>/', views.update_staff, name='update_staff'),
    path('delete-staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    # Branch Dashboard Urls
    path('branch/view-profile/', views.view_branch_profile, name='view_branch_profile'),
    path('branch/edit-profile/', views.edit_branch_profile, name='edit_branch_profile'),
    path('branch/delete-profile/', views.delete_branch_profile, name='delete_branch_profile'),

    # Staff Dashboard Urls
    path('staff/view-profile/', views.view_staff_profile, name='view_staff_profile'),
    path('staff/edit-profile/', views.edit_staff_profile, name='edit_staff_profile'),
    path('staff/delete-profile/', views.delete_staff_profile, name='delete_staff_profile'),
    path('staff/appointments/', views.view_appointments, name='view_appointments'),
    path('staff/appointments/update/<int:appointment_id>/', views.update_appointment, name='update_appointment'),

    # Services Urls(Client & Branch Dashboard)
    path('add-service/', views.add_service, name='add_service'),
    path('view-service/', views.view_services, name='view_services'),
    path('update-service/<int:service_id>/', views.update_service, name='update_service'),
    path('delete-service/<int:service_id>/', views.delete_service, name='delete_service'),

    # Customers Urls(Client & Branch Dashboard)
    path('add-customer/', views.add_customer, name='add_customer'),
    path('view-customer/', views.view_customers, name='view_customers'),
    path('update-customer/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('delete-customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    # Appointments Urls(Client & Branch Dashboard)
    path('add-appointment/', views.add_appointment, name='add_appointment'),
    path('view-appointment/', views.view_appointments, name='view_appointments'),
    path('update-appointment/<int:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('delete-appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
]