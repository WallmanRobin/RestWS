import gevent.monkey
import multiprocessing
gevent.monkey.patch_all()
bind = '0.0.0.0:8000'
# restart workers when code change, only use in development
#reload = True
preload_app = True
# debug when development and error when production
loglevel = 'error'
logfile = '/home/zouqiubin/python/RestWS/log/gunicorn.log'
accesslog = '/home/zouqiubin/python/RestWS/log/gunicorn.access'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
errorlog = '/home/zouqiubin/python/RestWS/log/gunicorn.err'
# process name
proc_name = 'vservice'
pidfile = '/home/zouqiubin/python/RestWS/log/gunicorn.pid'
# set process daemon, not use in default
#daemon = True
# number of processes
workers = multiprocessing.cpu_count() * 2 + 1
# number of threads of per process
threads = multiprocessing.cpu_count() * 2
worker_class = 'gevent'