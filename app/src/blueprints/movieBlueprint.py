from flask import Blueprint, Request, redirect, url_for, render_template, flash, request
from repository import MovieRepository, ActorRepository, ProducerRepository
from werkzeug.utils import secure_filename
from pymongo import database
from entity import Movie
from time import time
from os import remove as removeFile
from os.path import abspath, dirname, join

class MovieBlueprint(Blueprint):

    IMAGE_UPLOAD_FOLDER = join(abspath(dirname(__name__)), 'src/static/images/movies')

    __actorRepository: ActorRepository
    __movieRepository: MovieRepository
    __producerRepository: ProducerRepository

    def __init__(self, import_name: str, db: database.Database, **kwargs):
        super().__init__('movies', import_name, url_prefix="/movies", **kwargs)
        self.__actorRepository = ActorRepository(db.get_collection('actors'))
        self.__producerRepository = ProducerRepository(db.get_collection('producers'))
        self.__movieRepository = MovieRepository(db.get_collection('movies'), self.__actorRepository, self.__producerRepository)

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
                    request.form.getlist('producers'),
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
                if not self.isFormFullFilled(request, True):
                    flash('Some fields are missing in the form, try again', 'warn')
                    return redirect(url_for('movies.edit', id=movie['_id']))
                
                if (request.files['image'] != None or request.files['image'].filename != ''):
                
                    removeFile(join(self.IMAGE_UPLOAD_FOLDER, movie['image']))

                    image = request.files['image']
                    imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")

                self.__movieRepository.update(id, Movie(
                    request.form.get('title'),
                    request.form.get('release'),
                    request.form.getlist('actors'),
                    request.form.getlist('producers'),
                    request.form.get('description'),
                    imageName if imageName else movie['image']
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

    def isFormFullFilled(self, request: Request, imageIsPresent: bool = False) -> bool:
        for input in request.form:
            if request.form.get(input) in ['', None]:
                return False
                
        if not imageIsPresent and (request.files['image'] == None or request.files['image'].filename == ''):
            return False
        return True

    def getRoutes(self) -> dict:
        return {
            'movies.findAll',
            'movies.add',
            'movies.edit',
        }
