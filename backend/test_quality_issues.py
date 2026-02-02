# -*- coding: utf-8 -*-
"""
TEST FILE: Intentional code quality issues for Copilot review testing

This file demonstrates various code quality anti-patterns
"""

import json
import requests
import time

# CODE QUALITY ISSUE: Global variables
GLOBAL_COUNTER = 0
GLOBAL_CACHE = {}
USER_DATA = None

# CODE QUALITY ISSUE: Overly long function name that doesn't follow PEP 8
def ThisFunctionNameIsWayTooLongAndDoesntFollowPythonNamingConventionsAndMakesCodeHardToRead():
    """ISSUE: Function name violates PEP 8 guidelines"""
    pass

# CODE QUALITY ISSUE: Single letter variable names
def process(d, x, y, z):
    """ISSUE: Non-descriptive variable names"""
    a = x + y
    b = a * z
    c = b / 2
    return c

# CODE QUALITY ISSUE: Commented out code (code smell)
def calculate_total(items):
    """ISSUE: Large blocks of commented-out code"""
    total = 0
    # for item in items:
    #     total += item.price
    # return total * 1.1  # Old tax calculation
    
    # New implementation
    for item in items:
        total += item.price
    
    # if discount:
    #     total = total * 0.9
    # return total
    
    return total * 1.08

# CODE QUALITY ISSUE: Function with side effects not indicated in name
def get_user_profile(user_id):
    """
    ISSUE: Function name says 'get' but it modifies global state
    ISSUE: Side effects not documented
    """
    global USER_DATA
    global GLOBAL_COUNTER
    
    GLOBAL_COUNTER += 1  # ISSUE: Modifying global state
    
    # ISSUE: Making network call in function named 'get'
    response = requests.get(f"https://api.example.com/users/{user_id}")
    
    USER_DATA = response.json()  # ISSUE: Storing in global variable
    
    return USER_DATA

# CODE QUALITY ISSUE: Catching and ignoring exceptions
def load_config(filename):
    """ISSUE: Silent failure, swallowing exceptions"""
    try:
        with open(filename) as f:
            return json.load(f)
    except:
        pass  # ISSUE: Bare except with pass
    
    return {}  # ISSUE: Returning empty dict hides the error

# CODE QUALITY ISSUE: Not using context managers for resources
def read_file_unsafe(filename):
    """ISSUE: File handle may not be closed if exception occurs"""
    f = open(filename, 'r')
    data = f.read()
    # ISSUE: No guarantee file will be closed
    f.close()
    return data

# CODE QUALITY ISSUE: Duplicate code
def calculate_order_total_with_tax(items):
    """ISSUE: Duplicate logic"""
    subtotal = 0
    for item in items:
        subtotal += item.price * item.quantity
    tax = subtotal * 0.08
    return subtotal + tax

def calculate_invoice_total_with_tax(items):
    """ISSUE: Nearly identical to above function"""
    subtotal = 0
    for item in items:
        subtotal += item.price * item.quantity
    tax = subtotal * 0.08
    return subtotal + tax

# CODE QUALITY ISSUE: Function doing too many things
def process_and_save_and_notify_user(user_id, data, email, save_to_db, send_email, log_action):
    """
    ISSUE: Function name has 'and' multiple times - doing too much
    ISSUE: Too many boolean parameters
    ISSUE: Violates Single Responsibility Principle
    """
    # Process data
    processed = data.upper()
    
    # Save to database
    if save_to_db:
        # Database save logic
        pass
    
    # Send email
    if send_email:
        # Email sending logic
        pass
    
    # Log action
    if log_action:
        print(f"Action logged for user {user_id}")  # ISSUE: Using print instead of logger
    
    return processed

# CODE QUALITY ISSUE: Using eval() - dangerous practice
def calculate_expression(expression_string):
    """ISSUE: Using eval() is a security risk and code smell"""
    return eval(expression_string)

# CODE QUALITY ISSUE: Not using list comprehension where appropriate
def get_even_numbers(numbers):
    """ISSUE: Could be more Pythonic with list comprehension"""
    result = []
    for number in numbers:
        if number % 2 == 0:
            result.append(number)
    return result

# CODE QUALITY ISSUE: Comparing boolean to True/False explicitly
def is_valid_user(user):
    """ISSUE: Redundant boolean comparison"""
    if user.is_active == True:  # ISSUE: Should be just 'if user.is_active:'
        if user.is_verified == False:  # ISSUE: Should be 'if not user.is_verified:'
            return False
    return True

# CODE QUALITY ISSUE: Class with no methods (should be a dataclass or dict)
class UserConfig:
    """ISSUE: Class with only attributes, no behavior"""
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
        # Should use @dataclass instead
