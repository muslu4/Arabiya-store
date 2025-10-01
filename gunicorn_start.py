#!/usr/bin/env python
import os
import sys
import subprocess

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Change to backend directory
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

# Run gunicorn
subprocess.run([
    'gunicorn',
    '--bind', '0.0.0.0:8000',
    'ecom_project.wsgi:application'
])
