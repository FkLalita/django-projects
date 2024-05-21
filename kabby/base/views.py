from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView,ListView,TemplateView,View
from .forms import RideForm
from .models import Ride
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.


class RideListView(LoginRequiredMixin, ListView):
    model = Ride
    template_name = 'taxi/ride_list.html'

    def get_queryset(self):
        # Only return rides that belong to the logged-in user
        return self.model.objects.filter(passenger=self.request.user)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'taxi/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ride_count'] = Ride.objects.filter(passenger=self.request.user).count()
        context['completed_ride_count'] = Ride.objects.filter(passenger=self.request.user, is_completed=True).count()
        return context



class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    form_class = RideForm
    template_name = 'taxi/ride_create.html'
    success_url = reverse_lazy('taxi:ride_detail')

    def form_valid(self, form):
        # Set the passenger ID based on the logged-in user
        form.instance.passenger_id = self.request.user.id
        return super().form_valid(form)

class RideDetailView(LoginRequiredMixin, DetailView):
    model = Ride
    template_name = 'taxi/ride_detail.html'

    def get_queryset(self):
        # Only return rides that belong to the logged-in user
        return self.model.objects.filter(passenger=self.request.user)









class CustomLoginView(LoginView):
    template_name = 'taxi/login.html'
    success_url = reverse_lazy('taxi:dashboard')

    def form_valid(self, form):
        # Get the user object based on the username and password submitted in the form
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            # Log the user in and redirect them to the dashboard page
            login(self.request, user)
            return redirect(self.success_url)
        else:
            # Display an error message if the login credentials are invalid
            form.add_error(None, 'Invalid login credentials')
            return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('taxi:login')



class PassengerSignupView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'taxi/passenger_signup.html'
    success_url = reverse_lazy('taxi:login')

    def form_valid(self, form):
        # Save the user object
        response = super().form_valid(form)
        # Create a new PassengerProfile object and link it to the user
        PassengerProfile.objects.create(user=self.object)
        return response

class DriverSignupView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'taxi/driver_signup.html'
    success_url = reverse_lazy('taxi:login')

    def form_valid(self, form):
        # Save the user object
        response = super().form_valid(form)
        # Create a new DriverProfile object and link it to the user
        DriverProfile.objects.create(user=self.object)
        return response
    



class PaymentView(View):
    def get(self, request, *args, **kwargs):
        # Get the ride object to process payment for
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        # Check that the ride belongs to the logged-in user
        if ride.passenger != request.user:
            return redirect('taxi:ride_list')
        # Check that the ride has not already been completed
        if ride.is_completed:
            return redirect('taxi:ride_detail', pk=kwargs['pk'])
        # Render the payment form
        return render(request, 'taxi/payment.html', {'ride': ride})

    def post(self, request, *args, **kwargs):
        # Get the ride object to process payment for
        ride = get_object_or_404(Ride, pk=kwargs['pk'])
        # Check that the ride belongs to the logged-in user
        if ride.passenger != request.user:
            return redirect('taxi:ride_list')
        # Check that the ride has not already been completed
        if ride.is_completed:
            return redirect('taxi:ride_detail', pk=kwargs['pk'])
        # Process the payment
        payment_amount = ride.calculate_fare()
        payment_method = request.POST.get('payment_method')
        if payment_method == 'credit_card':
            # Process payment using a credit card payment API
            # ...
            ride.is_completed = True
            ride.save()
            return redirect('taxi:ride_detail', pk=kwargs['pk'])
        elif payment_method == 'paypal':
            # Process payment using PayPal API
            # ...
            ride.is_completed = True
            ride.save()
            return redirect('taxi:ride_detail', pk=kwargs['pk'])
        else:
            # Invalid payment method
            return render(request, 'taxi/payment.html', {'ride': ride, 'error': 'Invalid payment method'})
