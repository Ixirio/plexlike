from flask import Flask, redirect, url_for, render_template
from database import Database
from blueprints import MovieBlueprint, ActorBlueprint

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.jinja_env.add_extension('jinja2.ext.debug')
app.jinja_env.add_extension('jinja2.ext.i18n')

db = Database().getClient()

app.register_blueprint(MovieBlueprint(__name__, db))
app.register_blueprint(ActorBlueprint(__name__, db))

@app.route('/')
def home():
	return render_template('base.jinja')

# Route to handle 404 error and redirect user to home page
@app.errorhandler(404)
def page_not_found(e):
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
