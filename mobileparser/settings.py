import os

MONGO_DB_PORT = os.environ.get('OPENSHIFT_MONGODB_DB_PORT') or 24730
