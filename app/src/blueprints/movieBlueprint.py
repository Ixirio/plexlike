from flask import Blueprint, Request, jsonify, redirect, url_for, render_template, flash, request
from repository import MovieRepository, ActorRepository
from werkzeug.utils import secure_filename
from pymongo import database
from bson import json_util
from entity import Movie
from time import time
from json import loads as jsonLoads
from os import remove as removeFile
from os.path import abspath, dirname, join

class MovieBlueprint(Blueprint):

    IMAGE_UPLOAD_FOLDER = join(abspath(dirname(__name__)), 'src/static/images/movies')

    __actorRepository: ActorRepository
    __movieRepository: MovieRepository

    def __init__(self, import_name: str, db: database.Database, **kwargs):
        super().__init__('movies', import_name, url_prefix="/movies", **kwargs)
        self.__actorRepository = ActorRepository(db.get_collection('actors'))
        self.__movieRepository = MovieRepository(db.get_collection('movies'), self.__actorRepository)

        @self.route('/list', methods=['GET'])
        def findAll():
            return render_template('movies/list.jinja', movies=self.__movieRepository.findAll())

        @self.route('/<id>', methods=['GET'])
        def find(id):
            return render_template('movies/movie.jinja', movie=self.__movieRepository.findById(id))

        @self.route('/add', methods=['GET', 'POST'])
        def add():
            
            if request.method == 'POST':    
                if not self.isFormFullFilled(request):
                    flash('Some fields are missing in the form, try again', 'warn')
                    return redirect(url_for('movies.add'))
                
                image = request.files['image']
                imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")

                self.__movieRepository.insert(Movie(
                    request.form.get('title'),
                    request.form.get('release'),
                    request.form.getlist('actors'),
                    request.form.get('description'),
                    imageName
                ))

                image.save(join(self.IMAGE_UPLOAD_FOLDER, imageName))

                flash('Movie added sucessfully', 'info')
                return redirect(url_for('movies.findAll'))

            return render_template('movies/form.jinja', actors=self.__actorRepository.findAll())

        @self.route('/edit/<id>', methods=['GET', 'POST'])
        def edit(id):

            movie = self.__movieRepository.findById(id)

            if request.method == 'POST':    
                if not self.isFormFullFilled(request):
                    flash('Some fields are missing in the form, try again', 'warn')
                    return redirect(url_for('movies.edit'))
                
                removeFile(join(self.IMAGE_UPLOAD_FOLDER, movie['image']))
                
                image = request.files['image']
                imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")

                self.__movieRepository.update(id, Movie(
                    request.form.get('title'),
                    request.form.get('release'),
                    request.form.getlist('actors'),
                    request.form.get('description'),
                    imageName
                ))

                image.save(join(self.IMAGE_UPLOAD_FOLDER, imageName))

                flash('Movie updated sucessfully', 'info')
                return redirect(url_for('movies.findAll'))

            return render_template('movies/form.jinja', actors=self.__actorRepository.findAll(), movie=movie)

        @self.route('/remove/<id>', methods=['GET'])
        def remove(id):
            
            removeFile(join(self.IMAGE_UPLOAD_FOLDER, self.__movieRepository.findById(id)['image']))
            
            self.__movieRepository.remove(id)
            flash('Movie removed sucessfully', 'info')
            return redirect(url_for('movies.findAll'))

    def isFormFullFilled(self, request: Request) -> bool:
        form = request.form
        for input in form:
            if form.get(input) in ['', None] :
                return False
        if request.files['image'] == None or request.files['image'].filename == '':
            return False
        return True

    def getRoutes(self) -> dict:
        return {
            'movies.findAll',
            'movies.add',
            'movies.edit',
        }
