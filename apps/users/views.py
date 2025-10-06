from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserUpdateSerializer, UserProfileSerializer
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        # Send verification email
        send_verification_email(user)
        
        return Response({
            'message': 'User registered successfully. Please check your email for verification.',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Login user and return token."""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout user and delete token."""
    try:
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except:
        return Response({'message': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_profile(request):
    """Update current user profile."""
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': UserSerializer(request.user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_email(request, uidb64, token):
    """Verify user email."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)


def send_verification_email(user):
    """Send email verification to user."""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    subject = 'Verify your Smart Blind Stick account'
    message = f"""
    Hi {user.get_full_name()},
    
    Please click the link below to verify your account:
    http://localhost:8000/api/auth/verify/{uid}/{token}/
    
    Best regards,
    Smart Blind Stick Team
    """
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile management."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


# Template views for main pages
def landing_page(request):
    """Landing page view."""
    return render(request, 'landing.html')


@login_required
def dashboard(request):
    """User dashboard view."""
    try:
        return render(request, 'dashboard.html')
    except Exception as e:
        print(f"Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        return render(request, 'dashboard.html', {'error': str(e)})


def login_page(request):
    """Login page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        errors = []
        
        if not username:
            errors.append('Username is required')
        if not password:
            errors.append('Password is required')
            
        if not errors:
            from django.contrib.auth import authenticate, login
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                errors.append('Invalid username or password')
        
        return render(request, 'auth/login.html', {'errors': errors})
    
    return render(request, 'auth/login.html')


def register_page(request):
    """Registration page view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            # Handle form submission
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            role = request.POST.get('role')
            phone_number = request.POST.get('phone_number')
            visual_impairment_level = request.POST.get('visual_impairment_level')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_phone = request.POST.get('emergency_contact_phone')
            
            errors = []
            
            # Validation
            if not username:
                errors.append('Username is required')
            elif User.objects.filter(username=username).exists():
                errors.append('Username already exists')
                
            if not email:
                errors.append('Email is required')
            elif User.objects.filter(email=email).exists():
                errors.append('Email already exists')
                
            if not password:
                errors.append('Password is required')
            elif len(password) < 8:
                errors.append('Password must be at least 8 characters long')
                
            if password != password_confirm:
                errors.append('Passwords do not match')
                
            if not first_name:
                errors.append('First name is required')
                
            if not last_name:
                errors.append('Last name is required')
                
            if role == 'USER' and not visual_impairment_level:
                errors.append('Visual impairment level is required for users')
                
            if not errors:
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    phone_number=phone_number,
                    visual_impairment_level=visual_impairment_level,
                    emergency_contact_name=emergency_contact_name,
                    emergency_contact_phone=emergency_contact_phone
                )
                
                # Create user profile
                UserProfile.objects.create(user=user)
                
                # Login user
                from django.contrib.auth import login
                login(request, user)
                
                return redirect('dashboard')
            
            # If there are errors, render the form again with errors
            return render(request, 'auth/register.html', {'errors': errors})
            
        except Exception as e:
            # Log the error for debugging
            import traceback
            print(f"Registration error: {e}")
            traceback.print_exc()
            
            # Return form with error
            return render(request, 'auth/register.html', {
                'errors': [f'Registration failed: {str(e)}']
            })
    
    return render(request, 'auth/register.html')


@login_required
def profile_page(request):
    """User profile page view."""
    return render(request, 'profile.html')


def logout_page(request):
    """Logout page view."""
    from django.contrib.auth import logout
    logout(request)
    return redirect('landing')


def test_dashboard(request):
    """Test dashboard view without authentication."""
    return render(request, 'dashboard.html')


def placeholder_view(request):
    """Placeholder view for pages not yet implemented."""
    return render(request, 'placeholder.html', {
        'page_name': request.resolver_match.url_name.replace('_', ' ').title()
    })
