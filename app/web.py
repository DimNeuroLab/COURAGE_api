from flask import Blueprint, send_from_directory, render_template


web_blueprint = Blueprint("web", __name__)


@web_blueprint.route("/<path:path>", methods=["GET"])
def get_path(path):
    """serving static file for the webapp"""
    return send_from_directory("webapp", path)


@web_blueprint.route("/", methods=["GET"])
def get_root():
    """returns the main application page"""
    return render_template("courage_demo.html")


@web_blueprint.route("/twitter_demo", methods=["GET"])
def show_twitter_demo():
    """returns the twitter demo page"""
    return render_template("twitter_demo.html")


@web_blueprint.route("/algorithm_info", methods=["GET"])
def show_algorithm_info():
    """returns the algorithm info page"""
    return render_template("algorithm_info.html")
