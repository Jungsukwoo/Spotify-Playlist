from flask import Flask
from app.views.main_views import main_views
from app.views.analysis_views import analysis_views
from app.views.extract_views import extract_views
from app.views.recommendation_views import recommendation_views

app = Flask(
    __name__,
    static_folder="app/static",
    template_folder="app/templates"
)

app.register_blueprint(main_views)
app.register_blueprint(analysis_views)
app.register_blueprint(extract_views)
app.register_blueprint(recommendation_views)

if __name__ == "__main__":
    app.run(debug=True)