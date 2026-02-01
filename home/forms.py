from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import NewsletterSubscriber

User = get_user_model()


class SignupForm(UserCreationForm):
    """Custom signup form with additional fields."""
    
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-theme-primary focus:border-transparent',
            'placeholder': 'your.email@example.com'
        })
    )
    
    username = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    legal_name = forms.CharField(
        max_length=200,
        required=True,
        label="Legal name",
        help_text="Your name as it appears on government identification. Legal name is required to have on file for insurance and accounting purposes and will not be shared or printed for any purpose.",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-theme-primary focus:border-transparent',
            'placeholder': 'John Doe'
        })
    )
    
    nickname = forms.CharField(
        max_length=100,
        required=False,
        label="Nickname",
        help_text="How you'd like us to address you.",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-theme-primary focus:border-transparent',
            'placeholder': 'Johnny'
        })
    )
    
    subscribe_pycon_newsletter = forms.BooleanField(
        required=False,
        label="Subscribe to PyCon Nigeria Newsletter",
        help_text="Check this box to receive the PyCon Nigeria newsletter with announcements and information leading up to the conference.",
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-theme-primary border-gray-300 rounded focus:ring-theme-primary'
        })
    )
    
    subscribe_psf_newsletter = forms.BooleanField(
        required=False,
        label="Subscribe to Python Software Foundation Newsletter",
        help_text="Check this box to receive the Python Software Foundation newsletter. A quarterly newsletter informing you of important Python community news.",
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-theme-primary border-gray-300 rounded focus:ring-theme-primary'
        })
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-theme-primary focus:border-transparent',
            'placeholder': 'Enter your password'
        }),
        help_text="Your password can't be too similar to your other personal information. Your password must contain at least 8 characters. Your password can't be a commonly used password. Your password can't be entirely numeric."
    )
    
    password2 = forms.CharField(
        label="Password (again)",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-theme-primary focus:border-transparent',
            'placeholder': 'Confirm your password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'legal_name', 'nickname', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide username field - we'll use email as username
        if 'username' in self.fields:
            self.fields['username'].widget = forms.HiddenInput()
            self.fields['username'].required = False
    
    def clean_username(self):
        # Auto-generate username from email
        email = self.cleaned_data.get('email', '')
        if not email:
            # If email is not available yet, return empty string
            # It will be set in clean() method
            return ''
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        # Ensure username is set from email
        email = cleaned_data.get('email', '')
        if email:
            cleaned_data['username'] = email
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Ensure username and email are set correctly
        email = self.cleaned_data.get('email', '')
        user.username = email
        user.email = email
        
        # Store legal_name and nickname in user model if fields exist
        # Otherwise, we can use first_name and last_name as fallback
        if hasattr(user, 'first_name'):
            user.first_name = self.cleaned_data.get('legal_name', '')
        if hasattr(user, 'last_name'):
            user.last_name = self.cleaned_data.get('nickname', '')
        
        if commit:
            user.save()
            
            # Handle newsletter subscriptions
            email = self.cleaned_data['email']
            if self.cleaned_data.get('subscribe_pycon_newsletter'):
                NewsletterSubscriber.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
            if self.cleaned_data.get('subscribe_psf_newsletter'):
                # Note: PSF newsletter would need separate model or integration
                # For now, we'll just handle PyCon newsletter
                pass
        
        return user
