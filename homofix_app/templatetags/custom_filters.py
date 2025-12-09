from django import template
from homofix_app.models import SLOT_CHOICES

register = template.Library()

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter
def get_slot_display(slot_value):
    """Return the display value for a slot choice"""
    if slot_value is None:
        return ""
    
    # Convert to int if it's a string
    if isinstance(slot_value, str) and slot_value.isdigit():
        slot_value = int(slot_value)
    
    # Get the display value from SLOT_CHOICES
    for slot_id, display in SLOT_CHOICES:
        if slot_id == slot_value:
            return display
    
    return f"Slot {slot_value}"



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

