release: python api_ecommerce/manage.py migrate
web: gunicorn --chdir api_ecommerce api_ecommerce.wsgi --log-file -