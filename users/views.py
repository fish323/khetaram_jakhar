from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EmailSignupForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
# NEW IMPORTS FOR SECURITY LOGIC
from django.utils import timezone 
from datetime import timedelta

def ragister(request):
    if request.method == 'POST':
        form = EmailSignupForm(request.POST)
        if form.is_valid():
            # Save user but deactivate them until OTP verification
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            # Generate OTP (6 digits)
            otp = random.randint(100000, 999999)
            
            # Store user ID, OTP, TIMESTAMP, and ATTEMPTS in session
            request.session['verification_user_id'] = user.id
            request.session['verification_otp'] = otp
            # Store the current time (used for 5-minute expiry)
            request.session['verification_otp_timestamp'] = str(timezone.now()) 
            # Initialize attempts counter
            request.session['verification_otp_attempts'] = 0 

            # Send OTP via Email (Rest of the email logic remains the same)
            subject = 'Your Verification OTP'
            message = f'Your OTP for registration is {otp}. Please enter this to complete your signup.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            
            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                # Fallback for development if email fails
                print(f"Error sending email: {e}")
                print(f"OTP is: {otp}") 

            return redirect('verify_otp')
    else:
        form = EmailSignupForm()
    
    context = {
        'form': form
    }            
    return render(request, 'registration/signup.html', context)

def verify_otp(request):
    error_message = None
    MAX_ATTEMPTS = 3
    
    user_id = request.session.get('verification_user_id')
    session_otp = request.session.get('verification_otp')
    otp_timestamp_str = request.session.get('verification_otp_timestamp')
    otp_attempts = request.session.get('verification_otp_attempts', 0)

    # 1. Check if user data exists in session
    if not user_id or not session_otp or not otp_timestamp_str:
        return render(request, 'registration/verify_otp.html', {'error': "Session expired or invalid verification process started. Please register again."})

    # 2. OTP Expiry Check (5 minutes)
    otp_timestamp = timezone.datetime.fromisoformat(otp_timestamp_str)
    if timezone.now() > otp_timestamp + timedelta(minutes=5):
        # Clear session for security, forcing re-registration
        # The user account (is_active=False) remains, but they must start the flow again.
        if 'verification_user_id' in request.session: del request.session['verification_user_id']
        if 'verification_otp' in request.session: del request.session['verification_otp']
        if 'verification_otp_timestamp' in request.session: del request.session['verification_otp_timestamp']
        if 'verification_otp_attempts' in request.session: del request.session['verification_otp_attempts']
        return render(request, 'registration/verify_otp.html', {'error': "The OTP has expired (5 minutes limit). Please try registering again to receive a new OTP."})

    # 3. Rate-Limiting Check (3 attempts max)
    if otp_attempts >= MAX_ATTEMPTS:
        # Deactivate the account for security
        try:
            user_to_lock = User.objects.get(id=user_id)
            user_to_lock.is_active = False
            user_to_lock.save()
        except User.DoesNotExist:
            pass
            
        # Clear session to prevent further attempts
        if 'verification_user_id' in request.session: del request.session['verification_user_id']
        if 'verification_otp' in request.session: del request.session['verification_otp']
        if 'verification_otp_timestamp' in request.session: del request.session['verification_otp_timestamp']
        if 'verification_otp_attempts' in request.session: del request.session['verification_otp_attempts']

        return render(request, 'registration/verify_otp.html', {'error': f"Too many incorrect attempts. Your account is temporarily locked. Please try registering again."})


    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if str(entered_otp) == str(session_otp):
            # OTP Matches: Activate and log in the user
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            
            login(request, user)
            
            # Clear all session data on success
            if 'verification_user_id' in request.session: del request.session['verification_user_id']
            if 'verification_otp' in request.session: del request.session['verification_otp']
            if 'verification_otp_timestamp' in request.session: del request.session['verification_otp_timestamp']
            if 'verification_otp_attempts' in request.session: del request.session['verification_otp_attempts']
            
            return redirect('homeview')
        else:
            # OTP is incorrect - Increment attempt counter
            request.session['verification_otp_attempts'] = otp_attempts + 1
            attempts_remaining = MAX_ATTEMPTS - request.session['verification_otp_attempts']
            error_message = f"Invalid OTP. You have {attempts_remaining} attempts remaining."

    return render(request, 'registration/verify_otp.html', {'error': error_message})