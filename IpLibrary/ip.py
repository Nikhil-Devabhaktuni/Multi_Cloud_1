#Coustom library for sending mail to admin
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

current_timezone = timezone.get_current_timezone()


#for sednig emials
def send_login_notification(username, email,ip_address,location):
    subject = f'Login Notification: Successful Login to Your Account'
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    bcc_email=settings.EMAIL_RECEIVING_USER
    recipients = [email,bcc_email]
    message = f'Dear {username},\n\nWe wanted to inform you that a successful login was detected on your account.\n\nDate: {timestamp}\nLocation: {location}\nIP Address: {ip_address}\n\nIf you were the one who logged in, no further action is required.\n\nHowever, if you suspect any unauthorized access, please take the following steps:\n1. Change your password immediately.\n2. Review your account activity for any unusual actions.\n3. Enable two-factor authentication for added security.\n\nIf you have any concerns or need assistance, please contact our support team immediately from here {settings.EMAIL_RECEIVING_USER}.\n\nThank you for choosing us.\n\nBest regards,\nMultiCloud Security Team'
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=False)



def send_Alert_Notification(username, email,ip_address,location):
    subject = f'Security Alert: Unusual Login Attempt Detected for your Account'
    message = f'Dear {username},\n\nWe detected an unusual login attempt on your account.\n\nDate: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\nLocation: {location}\nIP Address: {ip_address}\n\nIf this was not you, please take immediate action:\n1. Change your password immediately.\n2. Review your account activity for any unauthorized access.\n3. Enable two-factor authentication for added security.\n\nIf you have any concerns or need assistance, please contact our support team immediately here {settings.EMAIL_RECEIVING_USER}.\n\nThank you for helping us keep your account secure.\n\nBest regards,\nMultiCloud Security Team'
    bcc_email=settings.EMAIL_RECEIVING_USER
    recipients = [email,bcc_email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=False)

def send_Wrong_Password_Notification(username, email, ip_address, location):
    subject = f'Login Attempt: Wrong Password for Your Account'
    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f'Dear {username},\n\nWe noticed an attempt to login to your account with the wrong password.\n\nDate: {timestamp}\nLocation: {location}\nIP Address: {ip_address}\n\nIf this was you, please double-check your password and try again.\n\nIf you suspect any unauthorized access, please take the following steps:\n1. Change your password immediately.\n2. Review your account activity for any unusual actions.\n3. Enable two-factor authentication for added security.\n\nIf you have any concerns or need assistance, please contact our support team immediately from here {settings.EMAIL_RECEIVING_USER}.\n\nThank you for choosing us.\n\nBest regards,\nMultiCloud Security Team'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)



