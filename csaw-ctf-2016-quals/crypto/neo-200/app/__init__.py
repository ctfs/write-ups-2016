from flask import Flask, render_template, request, redirect, abort, jsonify, json as json_mod, url_for
import logging
import os

def create_app():
    app = Flask("app", static_folder="static", template_folder="templates")
    with app.app_context():
        from app.views import init_views
        init_views(app)
        return app

