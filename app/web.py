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


@web_blueprint.route("/twitter_demo_it", methods=["GET"])
def show_italian_twitter_demo():
    """returns the twitter demo page"""
    return render_template("/italian_demo/italian_twitter_demo.html")


@web_blueprint.route("/twitter_demo_it_plain", methods=["GET"])
def show_italian_twitter_demo_plain():
    """returns the twitter demo page"""
    return render_template("/italian_demo/italian_twitter_demo_plain.html")


@web_blueprint.route("/twitter_demo_it_schools", methods=["GET"])
def show_italian_twitter_demo_schools():
    """returns the twitter demo page with fake news and misinformation decorations"""
    return render_template("/italian_demo/italian_twitter_demo_schools.html")


@web_blueprint.route("/twitter_demo_it_nb_e1", methods=["GET"])
def show_italian_twitter_demo_no_buttons_experiment1():
    """returns the twitter demo page without buttons for experiment 1"""
    return render_template("/italian_demo/italian_twitter_demo_nb_e1.html")


@web_blueprint.route("/twitter_demo_en_plain", methods=["GET"])
def show_english_twitter_demo_plain():
    """returns the English twitter demo page"""
    return render_template("/english_demo/english_twitter_demo_plain.html")


@web_blueprint.route("/twitter_demo_en_nb_e1", methods=["GET"])
def show_english_twitter_demo_no_buttons_experiment1():
    """returns the English twitter demo page without buttons for experiment 1"""
    return render_template("/english_demo/english_twitter_demo_nb_e1.html")


@web_blueprint.route("/algorithm_info", methods=["GET"])
def show_algorithm_info():
    """returns the algorithm info page"""
    return render_template("algorithm_info.html")
