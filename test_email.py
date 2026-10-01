#!/usr/bin/env python
"""
Test script to diagnose email configuration issues.
Run this from the project root: python test_email.py
"""

import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scope_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("EMAIL CONFIGURATION TEST")
print("=" * 60)

print(f"\n✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"✓ EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"✓ EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"✓ EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"✓ EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if not settings.EMAIL_HOST_USER:
    print("\n❌ ERROR: EMAIL_HOST_USER is empty!")
    print("   Make sure EMAIL_HOST_USER is set in your .env file")
    sys.exit(1)

if not settings.EMAIL_HOST_PASSWORD:
    print("\n❌ ERROR: EMAIL_HOST_PASSWORD is empty!")
    print("   Make sure EMAIL_HOST_PASSWORD is set in your .env file")
    sys.exit(1)

print("\n" + "=" * 60)
print("SENDING TEST EMAIL...")
print("=" * 60)

try:
    result = send_mail(
        subject='Test Email from SCOPE INDIA',
        message='If you received this email, your email configuration is working correctly!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['santhoshrs360@gmail.com'],
        fail_silently=False
    )
    print("\n✓ SUCCESS! Email sent successfully!")
    print(f"   Email was sent from: {settings.DEFAULT_FROM_EMAIL}")
    print(f"   Email was sent to: santhoshrs360@gmail.com")

except Exception as e:
    print(f"\n❌ ERROR: Email sending failed!")
    print(f"   Error Type: {type(e).__name__}")
    print(f"   Error Message: {str(e)}")
    print("\nPossible solutions:")
    print("1. Check that EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct in .env")
    print("2. For Gmail, use an App Password (not your regular password)")
    print("3. Ensure 2-Factor Authentication is enabled on your Gmail account")
    print("4. Check firewall/network settings (SMTP port 587 must be accessible)")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()
