# views/main_views.py
from flask import Blueprint, render_template

main_views = Blueprint("main_views", __name__)

@main_views.route("/")
def main_page():
    return render_template("MainPage.html")