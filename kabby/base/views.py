from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ride,Location,Driver,Wallet,Payment,Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm,RideForm,LocationForm,CompleteRideForm, EditDriverForm,AddDriverForm,EditProfileForm,FundWalletForm,PaymentForm

def home(request):
    if request.user.is_authenticated:
        return redirect('rides')
    else:
        return render(request, 'base/home.html')

@login_required
def profile(request):
    rides = Ride.objects.filter(passenger=request.user).order_by('-ride_created')
    return render(request, 'base/profile.html', {'rides': rides})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('rides')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'base/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('rides')
    else:
        form = SignUpForm()
    return render(request, 'base/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'base/edit_profile.html', {'form': form})

@login_required
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.user = request.user
            location.save()
            messages.success(request, 'Location added successfully!')
            return redirect('profile')
    else:
        form = LocationForm()
    return render(request, 'base/add_location.html', {'form': form})

@login_required
def location(request):
    location = Location.objects.all()
    return render(request, 'base/location.html', {'location': location})



@login_required
def edit_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id, user=request.user)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location updated successfully!')
            return redirect('profile')
    else:
        form = LocationForm(instance=location)
    return render(request, 'base/edit_location.html', {'form': form})

@login_required
def book_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.passenger = request.user
            ride.save()
            messages.success(request, 'Ride booked successfully!')
            return redirect('rides')
    else:
        form = RideForm()
    return render(request, 'base/book_ride.html', {'form': form})

@login_required
def Rides(request):
    ride = Ride.objects.all()
    return render(request, 'base/ride.html', {'ride': ride})



@login_required
def view_ride(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    return render(request, 'base/view_ride.html', {'ride': ride})

@login_required
def complete_ride(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id, driver=request.user)
    if request.method == 'POST':
        form = CompleteRideForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ride completed successfully!')
            return redirect('view_ride', ride_id=ride_id)
    else:
        form = CompleteRideForm(instance=ride)
    return render(request, 'base/complete_ride.html', {'form': form, 'ride': ride})

@login_required
def edit_driver(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    if request.method == 'POST':
        form = EditDriverForm(request.POST, instance=ride)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated successfully!')
            return redirect('view_ride', ride_id=ride_id)
    else:
        form = EditDriverForm(instance=ride)
    return render(request, 'base/edit_driver.html', {'form': form, 'ride': ride})



@login_required
def driver(request):
    drivers = Driver.objects.all()
    return render(request, 'base/driver.html', {'drivers': drivers})

@login_required
def add_driver(request):
    if request.method == 'POST':
        form = AddDriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver added successfully!')
            return redirect('driver')
    else:
        form = AddDriverForm()
    return render(request, 'base/add_driver.html', {'form': form})





@login_required
def fund_wallet(request):
    form = PaymentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet = Wallet.objects.get_or_create(user=request.user)[0]
            wallet.balance += amount
            wallet.save()
            messages.success(request, f'{amount:.2f} added to your wallet')
            return redirect('payment')
    return render(request, 'base/fund_wallet.html', {'form': form})



@login_required
def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = Payment(user=request.user, amount=form.cleaned_data['amount'])
            payment.save()
            messages.success(request, 'Payment successful!')
            return redirect('home')
    else:
        form = PaymentForm()
    return render(request, 'base/payment.html', {'form': form})
