import multiprocessing

num_workers = multiprocessing.cpu_count() * 2 + 1
command = '/virtualenvs/pythonizame/bin/gunicorn'
pythonpath = '/var/www_nginx/pythonizame'
bind = '0.0.0.0:8000'
workers = num_workers
timeout = 120
