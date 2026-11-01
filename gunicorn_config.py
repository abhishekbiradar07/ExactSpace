import os

# Gunicorn configuration file for Render
port = os.environ.get('PORT', '10000')
bind = f"0.0.0.0:{port}"

# Memory optimization
workers = 1
worker_class = 'sync'
threads = 2
timeout = 120

# Logging
loglevel = 'info'
accesslog = '-'
errorlog = '-'
capture_output = True

# Worker management
max_requests = 100
max_requests_jitter = 20
preload_app = False

# Print for debugging
print(f"Gunicorn binding to: {bind}")
print(f"PORT environment variable: {port}")
