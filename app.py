import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth
from auth.auth import AuthError, requires_auth
from flask_migrate import Migrate


def create_app(test_config=None):
    app = Flask(__name__)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)
    #oauth = OAuth(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,PUT,POST,DELETE,OPTIONS')
        return response


    #auth0 = oauth.register(
    #    'auth0',
    #    client_id='zNzK3s62YQ9xAx0RqkTfOWm7NN5U7SCe',
    #    client_secret='1EUaLZASC5yhg5mBABU19WeLwgEXtMt1CMNTHNd6dqbktVjHduPy5mpNXGVT4HQq',
    #    api_base_url='https://capstone-projects.auth0.com',
    #    access_token_url='https://capstone-projects.auth0.com/oauth/token',
    #    authorize_url='https://capstone-projects.auth0.com/authorize',
    #    client_kwargs={
    #        'scope': 'openid profile email',
    #        },
    #)


    @app.route('/')
    def health():
        return "Hello People!"


    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actor.query.order_by('id').all()

        if len(actors) == 0:
            abort(404)

        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            'actors': formatted_actors,
            'success': True
        }), 200


    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movie.query.order_by('id').all()

        if len(movies) == 0:
            abort(404)

        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            'movies': formatted_movies,
            'success': True
        }), 200


    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(422)

        try:
            if 'name' in body:
                actor.name = body['name']

            if 'age' in body:
                actor.age = body['age']

            if 'gender' in body:
                actor.gender = body['gender']

            actor.update()
            return jsonify({
                'success': True,
                'actors': [actor.format()]
            }), 200

        except Exception:
            abort(422)


    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)

        body = request.get_json()
        if body is None:
            abort(422)

        try:
            if 'title' in body:
                movie.title = body['title']

            if 'release_date' in body:
                movie.release_date = body['release_date']

            movie.update()
            return jsonify({
                'success': True,
                'movies': [movie.format()]
            }), 200

        except Exception:
            abort(422)


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(token):
        body = request.get_json()
        if body is None:
            abort(422)

        name = body.get('name', None)
        if name is None:
            abort(422)
        age = body.get('age', None)
        if age is None:
            abort(422)
        gender = body.get('gender', None)
        if gender is None:
            abort(422)

        try:
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
            new_id = new_actor.id
            return jsonify({
                'id': new_id,
                'success': True
            }), 201

        except Exception:
            abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(token):
        body = request.get_json()
        if body is None:
            abort(422)

        title = body.get('title', None)
        if(title is None):
            abort(422)
        release_date = body.get('release_date', None)
        if(release_date is None):
            abort(422)

        try:
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
            new_id = new_movie.id

            return jsonify({
                'id': new_id,
                'success': True
            }), 201

        except Exception:
            abort(422)


    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)

        try:
            actor.delete()
            return jsonify({
                'success': True
            }), 200

        except Exception:
            abort(422)


    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True
            }), 200

        except Exception:
            abort(422)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500


    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)