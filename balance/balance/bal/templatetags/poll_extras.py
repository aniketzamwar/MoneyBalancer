#!/usr/bin/python
from decimal import Decimal
from django import template
register = template.Library()

@register.filter    
def subtract(value, arg):
    return Decimal(value) - Decimal(arg)
