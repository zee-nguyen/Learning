from flask import Blueprint

bp = Blueprint("routes", __name__)


@bp.routes("/tasks", methods=["GET"])
def get_tasks():
    pass
