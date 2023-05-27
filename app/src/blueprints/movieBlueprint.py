from flask import Blueprint, Request, redirect, url_for, render_template, flash, request
from repository import MovieRepository, ActorRepository, ProducerRepository
from werkzeug.utils import secure_filename
from pymongo import database
from entity import Movie
from time import time
from os import remove as removeFile
from os.path import abspath, dirname, join, isfile
from services import FaceDetector
from services.transformer import CheckboxValueToBoolTransformer

class MovieBlueprint(Blueprint):

    IMAGE_UPLOAD_FOLDER = join(abspath(dirname(__name__)), 'src/static/images/movies')

    __actorRepository: ActorRepository
    __movieRepository: MovieRepository
    __producerRepository: ProducerRepository
    __checkboxValueToBoolTransformer: CheckboxValueToBoolTransformer

    def __init__(self, import_name: str, db: database.Database, **kwargs):
        super().__init__('movies', import_name, url_prefix="/movies", **kwargs)
        self.__actorRepository = ActorRepository(db.get_collection('actors'))
        self.__producerRepository = ProducerRepository(db.get_collection('producers'))
        self.__movieRepository = MovieRepository(db.get_collection('movies'), self.__actorRepository, self.__producerRepository)
        self.__checkboxValueToBoolTransformer = CheckboxValueToBoolTransformer()

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
                    flash('Some fields are missing in the form, try again', 'warning')
                    return redirect(url_for('movies.add'))

                image = request.files['image']
                imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")

                pathToImage = join(self.IMAGE_UPLOAD_FOLDER, imageName)
                try:
                    image.save(pathToImage)
                    if (self.__checkboxValueToBoolTransformer.transform(request.form.get('facedetection'))):
                        FaceDetector().detect(pathToImage)

                    self.__movieRepository.insert(Movie(
                        request.form.get('title'),
                        request.form.get('release'),
                        request.form.getlist('actors'),
                        request.form.getlist('producers'),
                        request.form.get('description'),
                        imageName
                    ))
                except:
                    return render_template('errors/error_500.html.jinja')

                flash('Movie added sucessfully', 'success')
                return redirect(url_for('movies.findAll'))

            return render_template('movies/form.jinja', actors=self.__actorRepository.findAll(), producers=self.__producerRepository.findAll())

        @self.route('/edit/<id>', methods=['GET', 'POST'])
        def edit(id):

            movie = self.__movieRepository.findById(id)

            if request.method == 'POST':    
                if not self.isFormFullFilled(request, True):
                    flash('Some fields are missing in the form, try again', 'warning')
                    return redirect(url_for('movies.edit', id=movie['_id']))

                if (request.files['image'].filename != ''):
                    pathToImage = join(self.IMAGE_UPLOAD_FOLDER, movie['image'])
                    if isfile(pathToImage): removeFile(pathToImage)

                    image = request.files['image']
                    imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")
                else:
                    image = None
                    imageName = movie['image']

                pathToImage = join(self.IMAGE_UPLOAD_FOLDER, imageName)

                try:
                    if (image is not None): image.save(pathToImage)

                    if (self.__checkboxValueToBoolTransformer.transform(request.form.get('facedetection'))):
                        FaceDetector().detect(pathToImage)

                    self.__movieRepository.update(id, Movie(
                        request.form.get('title'),
                        request.form.get('release'),
                        request.form.getlist('actors'),
                        request.form.getlist('producers'),
                        request.form.get('description'),
                        imageName
                    ))
                except:
                    return render_template('errors/error_500.html.jinja')

                flash('Movie updated sucessfully', 'success')
                return redirect(url_for('movies.findAll'))

            return render_template('movies/form.jinja', actors=self.__actorRepository.findAll(), producers=self.__producerRepository.findAll(), movie=movie)

        @self.route('/remove/<id>', methods=['GET'])
        def remove(id):

            removeFile(join(self.IMAGE_UPLOAD_FOLDER, self.__movieRepository.findById(id)['image']))

            self.__movieRepository.remove(id)
            flash('Movie removed sucessfully', 'success')
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
