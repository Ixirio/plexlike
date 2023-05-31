from flask import Blueprint, Request, redirect, url_for, render_template, flash, request
from repository import ProducerRepository
from entity import Producer
from pymongo import database
from werkzeug.utils import secure_filename
from os import remove as removeFile
from os.path import abspath, dirname, join, isfile
from time import time
from services import FaceDetector
from services.transformer import CheckboxValueToBoolTransformer

# ProducerBlueprint class
class ProducerBlueprint(Blueprint):

    IMAGE_UPLOAD_FOLDER = join(abspath(dirname(__name__)), 'src/static/images/producers')

    __producerRepository: ProducerRepository
    __checkboxValueToBoolTransformer: CheckboxValueToBoolTransformer

    # ProducerBlueprint constructor
    def __init__(self, import_name: str, db: database.Database, **kwargs):
        super().__init__('producers', import_name, url_prefix="/producers", **kwargs)
        self.__producerRepository = ProducerRepository(db.get_collection('producers'))
        self.__checkboxValueToBoolTransformer = CheckboxValueToBoolTransformer()

        # route to render all producers from database
        @self.route('/list', methods=['GET'])
        def findAll():
            return render_template('producers/list.jinja', producers=self.__producerRepository.findAll())

        # route to render a form to create a new producer
        @self.route('/add', methods=['GET', 'POST'])
        def add():
            if request.method == 'POST':    
                if not self.isFormFullFilled(request):
                    flash('Some fields are missing in the form, try again', 'warning')
                    return redirect(url_for('producers.add'))

                image = request.files['image']
                imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")
                pathToImage = join(self.IMAGE_UPLOAD_FOLDER, imageName)

                try:
                    image.save(pathToImage)
                    if (self.__checkboxValueToBoolTransformer.transform(request.form.get('facedetection'))):
                        FaceDetector().detect(pathToImage)

                    self.__producerRepository.insert(Producer(
                        request.form.get('firstname'),
                        request.form.get('lastname'),
                        imageName
                    ))
                except:
                    return render_template('errors/error_500.html.jinja')

                flash('Producer added sucessfully', 'success')
                return redirect(url_for('producers.findAll'))

            return render_template('producers/form.jinja')

        # route to handle producer edition
        @self.route('/edit/<id>', methods=['GET', 'POST'])
        def edit(id):

            producer = self.__producerRepository.findById(id)

            if request.method == 'POST':    
                if not self.isFormFullFilled(request, True):
                    flash('Some fields are missing in the form, try again', 'warn')
                    return redirect(url_for('producers.edit', id=producer['_id']))

                if (request.files['image'].filename != ''):
                    pathToImage = join(self.IMAGE_UPLOAD_FOLDER, producer['image'])
                    if isfile(pathToImage): removeFile(pathToImage)

                    image = request.files['image']
                    imageName = secure_filename(f"{int(time())}.{image.filename.split('.')[-1]}")
                else:
                    image = None
                    imageName = producer['image']

                pathToImage = join(self.IMAGE_UPLOAD_FOLDER, imageName)

                try:
                    if (image is not None): image.save(pathToImage)

                    if (self.__checkboxValueToBoolTransformer.transform(request.form.get('facedetection'))):
                        FaceDetector().detect(pathToImage)

                    self.__producerRepository.insert(Producer(
                        request.form.get('firstname'),
                        request.form.get('lastname'),
                        imageName
                    ))
                except:
                    return render_template('errors/error_500.html.jinja')

                flash('Producer updated sucessfully', 'success')
                return redirect(url_for('producers.findAll'))

            return render_template('producers/form.jinja', producer=producer)

        # route to handle producer deletion
        @self.route('/remove/<id>', methods=['GET'])
        def remove(id):
            removeFile(join(self.IMAGE_UPLOAD_FOLDER, self.__producerRepository.findById(id)['image']))

            self.__producerRepository.remove(id)
            flash('Producer removed sucessfully', 'success')
            return redirect(url_for('producers.findAll'))

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
            'producers.findAll',
            'producers.add',
            'producers.edit',
        }
