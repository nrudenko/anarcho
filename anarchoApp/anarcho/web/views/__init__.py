"""Anarcho REST blueprints"""
from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api")
