from flask import Blueprint, jsonify, redirect, url_for, flash, request
from repository import ActorRepository
from entity import Actor
from pymongo import database
from bson import json_util
import json

class ActorBlueprint(Blueprint):

    __actorRepository: ActorRepository

    def __init__(self, import_name: str, db: database.Database, **kwargs):
        super().__init__('actors', import_name, url_prefix="/actors", **kwargs)
        self.__actorRepository = ActorRepository(db.get_collection('actors'))

        @self.route('/list', methods=['GET'])
        def findAll():
            actors = self.__actorRepository.findAll()
            return jsonify(json.loads(json_util.dumps(actors)))

        @self.route('/<id>', methods=['GET'])
        def find(id):
            actor = self.__actorRepository.findById(id)
            return 'actor by id'

        @self.route('/add', methods=['GET', 'POST'])
        def add():
            
            # TODO : Check that form is complete
            if request.method == 'POST':
            
                self.__actorRepository.insert(Actor(
                    request.form.get('name'),
                    request.form.get('image')
                ))

                flash('Sucessfuly added actor', 'info')
                
            return redirect(url_for('actors.findAll'))

        @self.route('/<id>', methods=['POST'])
        def remove(id):
            self.__actorRepository.remove(id)
            return redirect(url_for('actors.findAll'))
