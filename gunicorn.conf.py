#!/usr/bin/env python3
"""
Gunicorn configuration for Coffee Shop Manager
"""

import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/home/u183730229/logs/gunicorn_access.log"
errorlog = "/home/u183730229/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "coffee_shop_gunicorn"

# Server mechanics
daemon = False
pidfile = "/home/u183730229/tmp/gunicorn.pid"
user = "u183730229"
group = "u183730229"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Preload app for better performance
preload_app = True


def when_ready(server):
    """Log when server is ready"""
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    """Log worker restart"""
    worker.log.info("worker received INT or QUIT signal")


def pre_fork(server, worker):
    """Log before forking"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def post_fork(server, worker):
    """Log after forking"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def post_worker_init(worker):
    """Log after worker initialization"""
    worker.log.info("Worker initialized (pid: %s)", worker.pid)
