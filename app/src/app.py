from flask import Flask, redirect, url_for
from database import Database
from blueprints import MovieBlueprint

app = Flask(__name__)

db = Database().getClient()

app.register_blueprint(MovieBlueprint(__name__, db))

@app.route('/')
def home():
	return 'Hello world'

# Route to handle 404 error and redirect user to home page
@app.errorhandler(404)
def page_not_found(e):
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
