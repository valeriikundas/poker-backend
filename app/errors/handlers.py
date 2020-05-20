from flask import jsonify

from app import db
from app.errors import blp


@blp.errorhandler(404)
def not_found_error(error):
    return jsonify({"status": "not found error"}), 404


@blp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"status": "internal error"}), 500
