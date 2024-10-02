from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseForbidden
from django.core.exceptions import ValidationError
from .models import User, SuperAdmin, Client, Branch, Service, Staff, Customer, Appointment
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

# Create your views here.

# Super Admin Signup View
@csrf_exempt
def super_admin_signup(request):
    if User.objects.filter(user_type='super_admin').exists():
        return JsonResponse({"message": "Super admin already exists. Please login "}, status=400)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if not password or not confirm_password or not email:
            return JsonResponse({"message": "All fields are required"}, status=400)
        
        if password != confirm_password:
            return JsonResponse({"message": "Passwords do not match"}, status=400)

        try:
            user = User.objects.create_user(username=email, password=password, email=email, user_type='super_admin')
            user.save()
            return JsonResponse({"message":"Super admin created successfully. Please login."}, status=201)
        except ValidationError as e:
            return JsonResponse({"message": str(e)}, status=400) 

    return render(request, 'super_admin/signup.html')                              

# Super Admin Login View
@csrf_exempt
def super_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == 'super_admin':
            login(request, user)
            return redirect('super_admin_dashbaord')
        else:
            return JsonResponse({"message": "Invalid credentials or not a super admin"}, status=400)
        
    return render(request, 'login.html')

# Client Signup View
@csrf_exempt
def client_signup(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        business_type = request.POST.get('bussiness')

        if not all([password, confirm_password, email, name, phone, business_type]):
            return JsonResponse({"message": "All fields are requires"}, status=400)
        
        if password != confirm_password:
            return JsonResponse({"message": "Passwords do not match"}, status=400)
        
        try:
            user = User.objects.create_user(username=email, password=password, email=email, user_type='admin')
            user.save()

            client = Client(admin=user, name=name, phone=phone, email=email, business_type=business_type)
            client.save()

            return JsonResponse({"message": "Client created successfully. Please login."}, status=201)
        except ValidationError as e:
            return JsonResponse({"message": str(e)}, status=400)
        
    return render(request, 'admin/signup.html') 

# Login view for super admin, client and staff
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Correct usage
            if user.user_type == 'super_admin':
                return redirect('super_admin_dashboard')
            elif user.user_type == 'admin':
                return redirect('admin_dashboard')  # Adjust as needed
            elif user.user_type == 'branch_admin':
                return redirect('branch_admin_dashboard')  # Adjust as needed
            elif user.user_type == 'staff':
                return redirect('staff_dashboard')
        else:
            return JsonResponse({"message": "Invalid credentials"}, status=400)

    return render(request, 'login.html')

# Logout view
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'login.html')     

# Super admin profile view
@login_required
def super_admin_profile(request):  
    if request.user.user_type != 'super_admin':
        return HttpResponseForbidden("You are not allowed to access this page.")

    super_admin = get_object_or_404(SuperAdmin, user=request.user)
    return render(request, 'super_admin_profile.html', {'super_admin': super_admin})
     
# Super admin edit profile
@login_required
def edit_super_admin_profile(request):
    if request.user.user_type != 'super_admin':
        return HttpResponseForbidden("You are not allowed to access this page.")

    super_admin = get_object_or_404(SuperAdmin, user=request.user)

    if request.method == 'POST':
        super_admin.name = request.POST.get('name')
        super_admin.phone = request.POST.get('phone')
        super_admin.save()

        request.user.email = request.POST.get('email')
        request.user.save()

        return redirect('super_admin_profile')

    return render(request, 'edit_super_admin_profile.html', {'super_admin': super_admin})

# Super admin delete profile
@login_required
def delete_super_admin_profile(request):
    if request.user.user_type != 'super_admin':
        return HttpResponseForbidden("You are not allowed to access this page.")

    super_admin = get_object_or_404(SuperAdmin, user=request.user)

    if request.method == 'POST':
        super_admin.delete()
        request.user.delete()

        return redirect('login')
    
    return render(request, 'delete_super_admin_profile.html', {'super_admin': super_admin})

# Super admin view for clients and their branches
@login_required
def view_clients(request):
    if request.user.user_type != 'super_admin':
        return HttpResponseForbidden("You are not allowed to access this page.")

    clients = Client.objects.prefetch_related('branch_set').all()
    return render(request, 'view_clients.html', {'clients': clients})    

# Client view profile
@login_required
def view_profile(request):

    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    client = get_object_or_404(Client, admin=request.user)

    return render(request, 'view_profile.html', {'client': client})

# Client edit profile
@login_required
def edit_profile(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    client = get_object_or_404(Client, admin=request.user)

    if request.method == 'POST':
        client.name = request.POST.get('name')
        client.phone = request.POST.get('phone')
        client.email = request.POST.get('email')
        client.place = request.POST.get('place')
        client.city = request.POST.get('city')
        client.state = request.POST.get('state')
        client.country = request.POST.get('country')
        client.business_type = request.POST.get('business_type')
        
        client.save()
        
        return redirect('view_profile')
    
    return render(request, 'edit_profile.html', {
        'client': client,
    })

# Client delete profile
@login_required
def delete_profile(request):
    # Check if the user is a client
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    client = get_object_or_404(Client, admin=request.user)
    
    if request.method == 'POST':
        client.delete()
        request.user.delete()  # Delete the user as well
        return redirect('login')  # Redirect to login page after deleting account
    
    return render(request, 'delete_profile.html', {
        'client': client,
    })

# Client adds branches and provide credentials
@login_required
@csrf_exempt
def add_branch(request):
    if request.user.user_type == 'admin':
        return HttpResponse("Unauthorized", status=401)
    
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        place = request.POST.get('place')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        if not all([client_id, username, password, name, phone, email, place, city, state, country]):
            return JsonResponse({"message": "All fields are required"}, status=400)

        try:    
            client = Client.objects.get(id=client_id)

            user = User.objects.create_user(username=username, password=password, email=email, user_type='branch_admin')
            user.save()

            branch = Branch(admin=user, client=client, name=name, phone=phone, email=email, place=place, city=city, state=state, country=country)
            branch.save()

            send_mail(
                'Branch Credentials',
                f'Your username is {username} and password is {password}.',
                'sandra002255@gmail.com',
                [email],
                fail_silently=False
            )   

            return JsonResponse({"message": "Branch created and credentials sent"}, status=201) 
        except Client.DoesNotExist:
            return JsonResponse({"message": "Client does not exist"}, status=400)
        
    return render(request, 'add_branch.html')   

# Allow clients to view their branches
@login_required
def view_branches(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branches = Branch.objects.filter(client_admin=request.user)
    return render(request, 'view_branches.html', {'branches': branches})

# Allow clients to edit their branches
@login_required
def update_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id, client__admin=request.user)

    if request.method == 'POST':
        branch.name = request.POST.get('name')
        branch.phone = request.POST.get('phone')
        branch.email = request.POST.get('email')
        branch.place = request.POST.get('place')
        branch.city = request.POST.get('city')
        branch.state = request.POST.get('state')
        branch.country = request.POST.get('country')
        branch.save()
        return redirect('view_branches')

    return render(request, 'update_branch.html', {'branch': branch})

# Allow clients to delete their branches
@login_required
def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id, client__admin=request.user)

    if request.method == 'POST':
        branch.delete()
        return redirect('view_branches')

    return render(request, 'delete_branch.html', {'branch': branch})

# Branches profile view
@login_required
def view_branch_profile(request):
    if request.user.user_type != 'branch_admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branch = get_object_or_404(Branch, admin=request.user)
    return render(request, 'view_branch_profile.html', {'branch': branch})

# Branches profile edit
@login_required
def edit_branch_profile(request):
    if request.user.user_type != 'branch_admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branch = get_object_or_404(Branch, admin=request.user)

    if request.method == 'POST':
        branch.name = request.POST.get('name')
        branch.phone = request.POST.get('phone')
        branch.email = request.POST.get('email')
        branch.place = request.POST.get('place')
        branch.city = request.POST.get('city')
        branch.state = request.POST.get('state')
        branch.country = request.POST.get('country')
        branch.save()
        return redirect('view_branch_profile')

    return render(request, 'edit_branch_profile.html', {'branch': branch})

# Branches profile delete
@login_required
def delete_branch_profile(request):
    if request.user.user_type != 'branch_admin':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branch = get_object_or_404(Branch, admin=request.user)

    if request.method == 'POST':
        branch.delete()
        return redirect('view_branch_profile')

    return render(request, 'delete_branch_profile.html', {'branch': branch})

# Add staff to client and branch
@login_required
def add_staff(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')

        if not all([username, password, name, email, phone, role]):
            return JsonResponse({"message": "All fields are required"}, status=400)
        
        # Create staff user
        user = User.objects.create_user(username=username, password=password, email=email, user_type='staff')
        user.save()

        staff = Staff(branch=Branch.objects.get(admin=request.user), user=user, name=name, email=email, phone=phone, role=role)
        staff.save()

        send_mail(
            'Staff Credentials',
            f'Your username is {username} and password is {password}.',
            'sandra002255@gmail.com',
            [email],
            fail_silently=False
        )

        return JsonResponse({"message": "Staff created and credentials sent"}, status=201)

    return render(request, 'add_staff.html')

# Allow clients and branch admins to view their staff
@login_required
def view_staff(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branch = get_object_or_404(Branch, admin=request.user)
    staff_members = Staff.objects.filter(branch=branch)

    return render(request, 'view_staff.html', {'staff_members': staff_members})

# Allow clients and branch admins to edit their staff
@login_required
def update_staff(request, staff_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        staff.name = request.POST.get('name')
        staff.email = request.POST.get('email')
        staff.phone = request.POST.get('phone')
        staff.role = request.POST.get('role')

        staff.save()
        return redirect('view_staff')

    return render(request, 'update_staff.html', {'staff': staff})

# Allow clients and branch admins to delete their staff
@login_required
def delete_staff(request, staff_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        staff.delete()
        return redirect('view_staff')

    return render(request, 'delete_staff.html', {'staff': staff})

# Staff profile view
@login_required
def view_staff_profile(request):
    if request.user.user_type != 'staff':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    staff = get_object_or_404(Staff, user=request.user)

    return render(request, 'view_staff_profile.html', {'staff': staff})

# Staff profile edit
@login_required
def edit_staff_profile(request):
    if request.user.user_type != 'staff':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == 'POST':
        staff.name = request.POST.get('name')
        staff.email = request.POST.get('email')
        staff.phone = request.POST.get('phone')
        staff.role = request.POST.get('role')

        staff.save()
        return redirect('view_staff_profile')

    return render(request, 'edit_staff_profile.html', {'staff': staff})

# Staff profile delete
@login_required
def delete_staff_profile(request):
    if request.user.user_type != 'staff':
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == 'POST':
        staff.delete()
        return redirect('login')

    return render(request, 'delete_staff_profile.html', {'staff': staff})

# Add service to branch and client
@login_required
def add_service(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        duration = request.POST.get('duration')

        if not all([branch_id, name, description, price, duration]):
            return JsonResponse({"message": "All fields are required"}, status=400)
        
        branch = get_object_or_404(Branch, id=branch_id)

        service = Service(branch=branch, name=name, description=description, price=price, duration=duration)
        service.save()

        return JsonResponse({"message": "Service added successfully"}, status=201)
    
    return render(request, 'add_service.html')

# View services in branch and client
@login_required
def view_services(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branch = get_object_or_404(Branch, admin=request.user)
    services = Service.objects.filter(branch=branch)

    return render(request, 'view_services.html', {'services': services})

# Edit service in branch and client
@login_required
def update_service(request, service_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.duration = request.POST.get('duration')

        service.save()
        
        return JsonResponse({"message": "Service updated successfully"}, status=201)
    
    return render(request, 'edit_service.html', {'service': service})

# Delete service in branch and client
@login_required
def delete_service(request, service_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service.delete()
        return JsonResponse({"message": "Service deleted successfully"}, status=201)

    return render(request, 'delete_service.html', {'service': service})

# Add Customer to branch and client
@login_required
def add_customer(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not all([branch_id, name, email, phone]):
            return JsonResponse({"message": "All fields are required"}, status=400)
        
        branch = get_object_or_404(Branch, id=branch_id)

        customer = Customer(branch=branch, name=name, email=email, phone=phone)
        customer.save()

        return JsonResponse({"message": "Customer added successfully"}, status=201)
    
    return render(request, 'add_customer.html')

# View customers in branch and client
@login_required
def view_customers(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branch = get_object_or_404(Branch, admin=request.user)
    customers = Customer.objects.filter(branch=branch)

    return render(request, 'view_customers.html', {'customers': customers}) 

# Edit customer in branch and client
@login_required
def update_customer(request, customer_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')

        customer.save()
        
        return JsonResponse({"message": "Customer updated successfully"}, status=201)
    
    return render(request, 'edit_customer.html', {'customer': customer})

# Delete customer in branch and client
@login_required
def delete_customer(request, customer_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return JsonResponse({"message": "Customer deleted successfully"}, status=201)

    return render(request, 'delete_customer.html', {'customer': customer})

# Add Appointment to branch and client
@login_required
def add_appointment(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        customer_id = request.POST.get('customer')
        staff_id = request.POST.get('staff')
        service_id = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')

        if not all([branch_id, customer_id, staff_id, service_id, date, time, status]):
            return JsonResponse({"message": "All fields are required"}, status=400)
        
        try:
            branch = Branch.objects.get(id=branch_id)
            customer = Customer.objects.get(id=customer_id)
            staff = Staff.objects.get(id=staff_id)
            service = Service.objects.get(id=service_id)
        
            appointment = Appointment(branch=branch, customer=customer, staff=staff, service=service, date=date, time=time, status=status)
            appointment.save()

            return JsonResponse({"message": "Appointment added successfully"}, status=201)

        except (Branch.DoesNotExist, Customer.DoesNotExist, Staff.DoesNotExist, Service.DoesNotExist):
            return JsonResponse({"message": "Invalid branch, customer, staff, or service"}, status=400)
        
    return render(request, 'add_appointment.html')

# View appointments in branch and client
@login_required
def view_appointments(request):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    branch = get_object_or_404(Branch, admin=request.user)
    appointments = Appointment.objects.filter(branch=branch)

    return render(request, 'view_appointments.html', {'appointments': appointments})

# Edit appointment in branch and client
@login_required
def update_appointment(request, appointment_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')

        appointment.save()
        
        return JsonResponse({"message": "Appointment updated successfully"}, status=201)
    
    return render(request, 'edit_appointment.html', {'appointment': appointment})

# Delete appointment in branch and client
@login_required
def delete_appointment(request, appointment_id):
    if request.user.user_type not in ['admin', 'branch_admin']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.delete()
        return JsonResponse({"message": "Appointment deleted successfully"}, status=201)

    return render(request, 'delete_appointment.html', {'appointment': appointment})

# Staff View Assigned Appointments
@login_required
def view_assigned_appointments(request):
    if request.user.user_type not in ['staff']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    staff = get_object_or_404(Staff, admin=request.user)
    appointments = Appointment.objects.filter(staff=staff)

    return render(request, 'view_assigned_appointments.html', {'appointments': appointments})

# Staff View Assigned appointment
@login_required
def view_assigned_appointment(request, appointment_id):
    if request.user.user_type not in ['staff']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, 'view_assigned_appointment.html', {'appointment': appointment})

# Staff Update Appointment
@login_required
def update_assigned_appointment(request, appointment_id):
    if request.user.user_type not in ['staff']:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')
        appointment.status = request.POST.get('status')

        appointment.save()
        
        return JsonResponse({"message": "Appointment updated successfully"}, status=201)
    
    return render(request, 'update_assigned_appointment.html', {'appointment': appointment})

