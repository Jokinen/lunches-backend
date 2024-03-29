#!/usr/bin/python
import os

virtenv = os.environ.get('OPENSHIFT_PYTHON_DIR', '') + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

from rest.app import app as application

# OpenShift support: bind to OpenShift environment variables if available
host = os.environ.get('OPENSHIFT_PYTHON_IP', 'localhost')
port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', '5000'))

if __name__ == '__main__':
    application.run(host=host, port=port)

#
# Below for testing only
#
# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     httpd = make_server('localhost', 8051, application)
#     # Wait for a single request, serve it and quit.
#     httpd.serve_forever()
