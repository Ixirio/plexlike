from flask import Blueprint, jsonify, redirect, url_for
from repository import MovieRepository
from entity import Movie
from pymongo import database
from bson import json_util
import json

class MovieBlueprint(Blueprint):

    __movieRepository: MovieRepository

    def __init__(self, import_name: str, db: database.Database, **kwargs):
        super().__init__('movies', import_name, url_prefix="/movies", **kwargs)
        self.__movieRepository = MovieRepository(db.get_collection('movies'))

        @self.route('/list', methods=['GET'])
        def findAll():
            movies = self.__movieRepository.findAll()
            return jsonify(json.loads(json_util.dumps(movies)))

        @self.route('/<id>', methods=['GET'])
        def find(id):
            movie = self.__movieRepository.findById(id)
            return 'movie by id'

        @self.route('/add', methods=['POST'])
        def add_get():
            self.__movieRepository.insert(Movie('avatar2', '2023-05-04', ['123456789012345678901234', '123456789012345678901234']))
            return 'added movie'

        @self.route('/add', methods=['GET'])
        def add_post():
            return 'add a movie'

        @self.route('/<id>', methods=['POST'])
        def remove(id):
            self.__movieRepository.remove(id)
            return redirect(url_for('movies.findAll'))
