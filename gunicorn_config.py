import os
import multiprocessing

# Gunicorn configuration file - optimized for Render free tier (512MB)
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
workers = 1  # Single worker to save memory
worker_class = 'sync'
threads = 2  # Use threads instead of workers
timeout = 120
loglevel = 'info'
accesslog = '-'
errorlog = '-'
max_requests = 100  # Recycle workers to prevent memory leaks
max_requests_jitter = 20
preload_app = False  # Don't preload to save memory during startup
