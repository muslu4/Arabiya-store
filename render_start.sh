#!/bin/bash
cd backend
gunicorn ecom_project.wsgi:application