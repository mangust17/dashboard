# -*- coding: utf-8 -*-
import os
import sys

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "6"
os.environ["VECLIB_MAXIMUM_THREADS"] = "4" 
os.environ["NUMEXPR_NUM_THREADS"] = "6"


sys.path.insert(0, '/var/www/u3117648/data/www/optone-partners.ru/dashboard')
sys.path.insert(1, '/var/www/u3117648/data/www/optone-partners.ru/djangoenvv/lib/python3.10/site-packages/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dashsite.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
