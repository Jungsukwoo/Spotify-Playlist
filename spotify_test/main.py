# main.py
from flask import Flask
from app.views.main_views import main_views
from app.views.extract_views import extract_views

app = Flask(__name__, template_folder="app/templates")
app.register_blueprint(main_views)
app.register_blueprint(extract_views)

if __name__ == "__main__":
    app.run(debug=True)