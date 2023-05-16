from flask import Flask, redirect, url_for, render_template
from database import Database
from blueprints import MovieBlueprint, ActorBlueprint
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.jinja_env.add_extension('jinja2.ext.debug')
app.jinja_env.add_extension('jinja2.ext.i18n')

db = Database().getClient()

movieBlueprint = MovieBlueprint(__name__, db)
actorBlueprint = ActorBlueprint(__name__, db)

function = {
	'movies_routes': movieBlueprint.getRoutes,
	'actors_routes': actorBlueprint.getRoutes
}

app.register_blueprint(movieBlueprint)
app.register_blueprint(actorBlueprint)

app.jinja_env.globals.update(function)


@app.route('/')
def home():
	return render_template('base.jinja')

# Route to handle 404 error and redirect user to home page
@app.errorhandler(404)
def page_not_found(e):
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
