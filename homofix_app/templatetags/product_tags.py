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