from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import views as auth_views

# Create your views here.


def home(request):
    context = {
        'property_types': PROPERTY_TYPES,
    }
    return render(request, 'index.html', context)


def listing(request):
    # Get the form data
    keyword = request.GET.get('keyword', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Start filtering the properties based on form input
    properties = Property.objects.prefetch_related('images').all()

    if keyword:
        properties = properties.filter(title__icontains=keyword)

    if category:
        properties = properties.filter(property_type=category)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    # Pass the filtered properties to the template
    context = {
        'properties': properties,
        'property_types': PROPERTY_TYPES,
    }

    return render(request, 'listing.html', context)


def property_detail(request, id):
    # Fetch the specific property using the property_id
    property = get_object_or_404(Property, id=id)
    
    if request.method == 'POST':
        message = request.POST['message']
        contact_info = request.POST['contact_info']

        Inquiry.objects.create(
            property=property,
            user=request.user,
            message=message,
            contact_info=contact_info
        )
        return redirect('property_detail', id=property.id)

    # Fetch all images for the property
    property_images = PropertyImage.objects.filter(property=property)

    # Fetch related properties (this could be properties of the same type or similar location)
    related_properties = Property.objects.filter(
        property_type=property.property_type).exclude(id=property.id)[:3]

    context = {
        'property': property,
        'property_images': property_images,
        'related_properties': related_properties,
    }

    return render(request, 'property_detail.html', context)


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phone_number']
        is_owner = 'is_owner' in request.POST
        is_agent = 'is_agent' in request.POST

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(
            username=email, email=email, password=password, first_name=first_name)

        # Create the profile for the user
        profile = Profile.objects.create(
            user=user,
            phone_number=phone_number,
            is_owner=is_owner,
            is_agent=is_agent
        )

        # Log the user in after registration
        login(request, user)

        # Redirect to a success page or user dashboard
        return redirect('home')  # Update this with your post-signup route

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        remember_me = 'remember_me' in request.POST

        # Authenticate user
        print(email,password)
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # If remember_me is checked, set session expiry to 0 (persistent session)
            if remember_me:
                request.session.set_expiry(0)
            else:
                # Session expires in 2 weeks
                request.session.set_expiry(1209600)

            # Redirect to homepage or dashboard after login
            return redirect('home')  # Update this to your post-login page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def property_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        property_type = request.POST.get('property_type')
        transaction_type = request.POST.get('transaction_type')
        price = request.POST.get('price')
        location = request.POST.get('location')
        area_sq_ft = request.POST.get('area_sq_ft')
        number_of_rooms = request.POST.get('number_of_rooms')
        amenities = request.POST.get('amenities')
        status = request.POST.get('status')

        property_instance = Property.objects.create(
            owner=request.user.profile,
            title=title,
            description=description,
            property_type=property_type,
            transaction_type=transaction_type,
            price=price,
            location=location,
            area_sq_ft=area_sq_ft,
            number_of_rooms=number_of_rooms,
            amenities=amenities,
            status=status
        )

        # Handling multiple image uploads
        images = request.FILES.getlist('images')
        for image in images:
            PropertyImage.objects.create(
                property=property_instance, image=image)

        return redirect('property_detail', id=property_instance.pk)

    # For choices in the form, you can pass lists to the template
    return render(request, 'list_form.html', {
        'property_types': PROPERTY_TYPES,
        'transaction_types': TRANSACTION_TYPES,
        'listing_status': LISTING_STATUS
    })


class CustomLogoutView(auth_views.LogoutView):
    http_method_names = ['get', 'post']
