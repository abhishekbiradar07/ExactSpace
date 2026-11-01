#!/bin/bash
echo "Starting RAG System..."
echo "PORT is: $PORT"
exec gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --workers 1 --timeout 120 --log-level info
