from flask import Flask, redirect, url_for, render_template
from database import Database
from blueprints import MovieBlueprint, ActorBlueprint, ProducerBlueprint
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
# secret key required for flash messages
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# debug extensions
app.jinja_env.add_extension('jinja2.ext.debug')
app.jinja_env.add_extension('jinja2.ext.i18n')

db = Database().getClient()

movieBlueprint = MovieBlueprint(__name__, db)
actorBlueprint = ActorBlueprint(__name__, db)
producerBlueprint = ProducerBlueprint(__name__, db)

# function to add in jinja templates
function = {
	'movies_routes': movieBlueprint.getRoutes,
	'actors_routes': actorBlueprint.getRoutes,
	'producers_routes': producerBlueprint.getRoutes
}

app.register_blueprint(movieBlueprint)
app.register_blueprint(actorBlueprint)
app.register_blueprint(producerBlueprint)

# adding functions to jinja templates
app.jinja_env.globals.update(function)

@app.route('/')
def home():
	return redirect(url_for('movies.findAll'))

# Route to handle 404 error and redirect user to movies list
@app.errorhandler(404)
def page_not_found(e):
	return redirect(url_for('movies.findAll'))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
