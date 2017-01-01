# -*- coding: utf-8 -*-

import os

restaurantMenuSchema = {
    'opening_times': {
        'type': 'dict',
        'schema': {
            'type': 'list'
        }
    },
    'name': {
        'type': 'string'
    }
}

daySchema = {
    'year': {
        'type': 'int'
    },
    'month': {
        'type': 'int'
    },
    'day': {
        'type': 'int'
    },
    'week_number': {
        'type': 'string'
    },
    'week_day': {
        'type': 'int'
    },
    'restaurants': {
        'type': 'list',
        'schema': restaurantMenuSchema
    }
}

DOMAIN = {
    'days': {
        'schema': daySchema
    }
}

settings = {
    'MONGO_HOST': os.environ.get('OPENSHIFT_MONGODB_DB_HOST', 'localhost'),
    'MONGO_PORT': os.environ.get('OPENSHIFT_MONGODB_DB_PORT', 27017),
    'MONGO_USERNAME': os.environ.get('OPENSHIFT_MONGODB_DB_USERNAME', ''),
    'MONGO_PASSWORD': os.environ.get('OPENSHIFT_MONGODB_DB_PASSWORD', ''),
    'MONGO_DBNAME': 'safkat',

    'RESOURCE_METHODS': ['GET'],

    'CACHE_CONTROL': 'max-age=20',
    'CACHE_EXPIRES': 20,

    'XML': False,

    'DOMAIN': DOMAIN
}
