from flask import Blueprint, Request, redirect, url_for, render_template, flash, request
from repository import ActorRepository
from entity import Actor
from pymongo import database
from werkzeug.utils import secure_filename
from os import remove as removeFile
from os.path import abspath, dirname, join, isfile
from time import time
from services import FaceDetector
from services.transformer import CheckboxValueToBoolTransformer

# ActorBlueprint class
class ActorBlueprint(Blueprint):

    IMAGE_UPLOAD_FOLDER = join(abspath(dirname(__name__)), 'src/static/images/actors')

    __actorRepository: ActorRepository
    __checkboxValueToBoolTransformer: CheckboxValueToBoolTransformer

    # ActorBlueprint constructor
    def __init__(self, import_name: str, db: database.Database, **kwargs):
        super().__init__('actors', import_name, url_prefix="/actors", **kwargs)
        self.__actorRepository = ActorRepository(db.get_collection('actors'))
        self.__checkboxValueToBoolTransformer = CheckboxValueToBoolTransformer()

        # route to render all actors from database
        @self.route('/list', methods=['GET'])
        def findAll():
            return render_template('actors/list.jinja', actors=self.__actorRepository.findAll())

        # route to render a form to create a new actor
        @self.route('/add', methods=['GET', 'POST'])
        def add():
            if request.method == 'POST':    
                if not self.isFormFullFilled(request):
                    flash('Some fields are missing in the form, try again', 'warning')
                    return redirect(url_for('actors.add'))

                image = request.files['image']
                imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")

                pathToImage = join(self.IMAGE_UPLOAD_FOLDER, imageName)

                try:
                    image.save(pathToImage)
                    if (self.__checkboxValueToBoolTransformer.transform(request.form.get('facedetection'))):
                        FaceDetector().detect(pathToImage)
                    self.__actorRepository.insert(Actor(
                        request.form.get('firstname'),
                        request.form.get('lastname'),
                        imageName
                    ))
                except:
                    return render_template('errors/error_500.html.jinja')

                flash('Actor added sucessfully', 'success')
                return redirect(url_for('actors.findAll'))

            return render_template('actors/form.jinja')

        # route to handle actor edition
        @self.route('/edit/<id>', methods=['GET', 'POST'])
        def edit(id):

            actor = self.__actorRepository.findById(id)

            if request.method == 'POST':    
                if not self.isFormFullFilled(request, True):
                    flash('Some fields are missing in the form, try again', 'warning')
                    return redirect(url_for('actors.edit', id=actor['_id']))

                if (request.files['image'].filename != ''):
                    pathToImage = join(self.IMAGE_UPLOAD_FOLDER, actor['image'])
                    if isfile(pathToImage): removeFile(pathToImage)

                    image = request.files['image']
                    imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")
                else:
                    image = None
                    imageName = actor['image']

                pathToImage = join(self.IMAGE_UPLOAD_FOLDER, imageName)

                try:
                    if (image is not None): image.save(pathToImage)

                    if (self.__checkboxValueToBoolTransformer.transform(request.form.get('facedetection'))):
                        FaceDetector().detect(pathToImage)

                    self.__actorRepository.update(id, Actor(
                        request.form.get('firstname'),
                        request.form.get('lastname'),
                        imageName
                    ))
                except:
                    return render_template('errors/error_500.html.jinja')

                flash('Actor updated sucessfully', 'success')
                return redirect(url_for('actors.findAll'))

            return render_template('actors/form.jinja', actor=actor)

        # route to handle actor deletion
        @self.route('/remove/<id>', methods=['GET'])
        def remove(id):
            removeFile(join(self.IMAGE_UPLOAD_FOLDER, self.__actorRepository.findById(id)['image']))

            self.__actorRepository.remove(id)
            flash('Actor removed sucessfully', 'success')
            return redirect(url_for('actors.findAll'))

    # method to check that each fields of the form are fullfilled
    def isFormFullFilled(self, request: Request, imageIsPresent: bool = False) -> bool:
        for input in request.form:
            if request.form.get(input) in ['', None]:
                return False

        if not imageIsPresent and (request.files['image'] == None or request.files['image'].filename == ''):
            return False
        return True

    def getRoutes(self) -> dict:
        return {
            'actors.findAll',
            'actors.add',
            'actors.edit',
        }
