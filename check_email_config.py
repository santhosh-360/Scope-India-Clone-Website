#!/usr/bin/env python
"""Quick email configuration check"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

# Load env vars
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

print("=" * 60)
print("ENVIRONMENT VARIABLES CHECK")
print("=" * 60)

email_host_user = os.getenv('EMAIL_HOST_USER')
email_host_password = os.getenv('EMAIL_HOST_PASSWORD')
secret_key = os.getenv('SECRET_KEY')

print(f"\nENVIRONMENT VARIABLES LOADED:")
print(f"  EMAIL_HOST_USER: {email_host_user}")
print(f"  EMAIL_HOST_PASSWORD: {'*' * len(email_host_password) if email_host_password else 'NOT SET'}")
print(f"  SECRET_KEY: {secret_key[:20]}..." if secret_key else "  SECRET_KEY: NOT SET")

if not email_host_user:
    print("\n❌ Problem: EMAIL_HOST_USER is not set in .env")
if not email_host_password:
    print("\n❌ Problem: EMAIL_HOST_PASSWORD is not set in .env")

print("\n" + "=" * 60)
print("EMAIL CONFIGURATION IN DJANGO SETTINGS")
print("=" * 60)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scope_project.settings')
django.setup()

from django.conf import settings

print(f"\n  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

if not settings.EMAIL_HOST_USER:
    print("\n❌ Problem: EMAIL_HOST_USER is None in Django settings")
    print("   The environment variable might not be loaded properly")

if not settings.EMAIL_HOST_PASSWORD:
    print("\n❌ Problem: EMAIL_HOST_PASSWORD is None in Django settings")
    print("   The environment variable might not be loaded properly")

print("\n" + "=" * 60)
print("GMAIL APP PASSWORD REQUIREMENT")
print("=" * 60)
print("""
⚠️  IMPORTANT FOR GMAIL:

Gmail does NOT allow using your regular password with SMTP.
You MUST use an App Password (16 characters) instead.

Steps to get an App Password:
1. Go to https://myaccount.google.com
2. Click "Security" in the left menu
3. Enable "2-Step Verification" (if not already enabled)
4. Under "App passwords", select:
   - App: "Mail"
   - Device: "Windows Computer" (or your device)
5. Click "Generate"
6. Copy the 16-character password
7. Update your .env file with this password

Your current .env EMAIL_HOST_PASSWORD looks like: {email_host_password}
Length: {len(email_host_password) if email_host_password else 0} characters
Expected: 16 characters (without spaces)
""")

if email_host_password and len(email_host_password) != 16:
    print(f"❌ WARNING: Your password is {len(email_host_password)} characters")
    print("   But Gmail App Passwords should be exactly 16 characters!")
    print("   Please regenerate a new App Password from Gmail")
