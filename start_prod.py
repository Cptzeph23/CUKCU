import os
import sys

# Add your project to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CUKCU1.settings')

import django
from django.core.wsgi import get_wsgi_application

django.setup()
application = get_wsgi_application()

if __name__ == '__main__':
    from gunicorn.app.base import Application


    class DjangoApplication(Application):
        def __init__(self):
            self.usage = None
            self.prog = None
            self.cfg = None
            self.config_file = ""
            self.callable = None
            self.project_path = os.path.dirname(os.path.abspath(__file__))
            self.logger = None
            self.do_load_config()

        def init(self, parser, opts, args):
            pass

        def load_config(self):
            self.cfg = self.configurable.Config()

            # Get port from environment or default to 8000
            port = os.environ.get('PORT', '8000')
            if not port.isdigit():
                port = '8000'

            self.cfg.set('bind', f'0.0.0.0:{port}')
            self.cfg.set('workers', 1)
            self.cfg.set('accesslog', '-')
            self.cfg.set('errorlog', '-')

        def load(self):
            return application


    DjangoApplication().run()