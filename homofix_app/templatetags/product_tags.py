from django import template
from decimal import Decimal
register = template.Library()

@register.simple_tag
def call_sellprice(price,quantity):
    sell_price = price*quantity
    return sell_price

@register.simple_tag
def call_gst(subtotal):
    total_amt = (call_sellprice*18)/100
    return total_amt


@register.simple_tag
def call_sellprice(price, quantity):
    amt= Decimal(price) * Decimal(quantity)
    amt += (amt*18)/100
    return amt

@register.simple_tag
def call_subtotal(total, tax):
    totl= float(total + tax)
    
    return totl


@register.simple_tag
def call_gsthalf(price, quantity):
    amt = call_sellprice(price, quantity)
    half_tax = (amt * 9) / 100 / 2
    return half_tax


@register.simple_tag
def call_addon_amt_invoice(quantity,rate):
    amt = quantity*rate
    return amt

@register.simple_tag
def call_amt_invoice(quantity,rate):
    amt = quantity*rate
    return amt
    
    
    

@register.simple_tag
def call_subtotal_invoice(total_amt,coupon_disc):
    amt = float(total_amt + coupon_disc)
    return amt

import base64
import os
from django.conf import settings

@register.simple_tag
def get_logo_base64():
    """
    Returns the base64 data URI of the logo for PDF generation 
    so wkhtmltopdf doesn't need to make network requests.
    """
    try:
        # Check common logo paths in the project (both local and production paths)
        paths_to_check = [
            os.path.join(settings.BASE_DIR, 'homofix_app', 'static', 'assets', 'images', 'logodark.png'),
            os.path.join(settings.BASE_DIR, 'homofix_app', 'static', 'logodark.png'),
            os.path.join(settings.BASE_DIR, 'static', 'assets', 'images', 'logodark.png'),
            os.path.join(settings.BASE_DIR, 'static', 'logodark.png'),
            os.path.join(settings.BASE_DIR, 'logodark.png'),
            # Fallback for the absolute path previously used on the ubuntu server
            '/home/ubuntu/homofix/static/logodark.png',
            '/home/ubuntu/homofix/homofix_app/static/assets/images/logodark.png',
            '/home/ubuntu/homofix/homofix_app/static/logodark.png'
        ]
        
        for logo_path in paths_to_check:
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    return f"data:image/png;base64,{encoded_string}"
        
        return "" # If not found, return empty string
    except Exception as e:
        print(f"Error encoding logo to base64: {e}")
        return ""