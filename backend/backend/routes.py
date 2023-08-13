from flask import Blueprint, current_app

bp = Blueprint("routes", __name__)


@bp.route("/test")
def test():
    return "test"
