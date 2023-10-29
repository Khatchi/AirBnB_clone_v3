#!/usr/bin/python3
"""Defines api index"""

from api.v1.views import app_views

@app_views.route('/status')
def get_status():
    """Returns current status of api"""
    return {'status': 'OK'}
# Task3 ended here