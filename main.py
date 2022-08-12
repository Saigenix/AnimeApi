from ast import Delete
from email import message
from flask import Flask, request,make_response,render_template
from flask_restful import Api,Resource , reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///animes.db'
db = SQLAlchemy(app)


class AnimeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(1000),nullable=False)
    anime_url = db.Column(db.String(900),nullable=False)
    
    def __repr__(self) -> str:
        return f"AnimeModel('{name}','{description}','{anime_url}')"


#db.create_all()
anime_put_args = reqparse.RequestParser()
anime_put_args.add_argument('title', type=str, required=True, help='Title cannot be blank')
anime_put_args.add_argument('description', type=str, required=True, help='Title cannot be blank')
anime_put_args.add_argument('image_url', type=str, required=True, help='Title cannot be blank')


# Animes ={}
# def abort_if_anime_id_doesnt_exist(anime_id):
#     if anime_id not in Animes:
#         abort(404, message="Anime {} doesn't exist".format(anime_id))
        
# def abort_if_anime_id_exists(anime_id):
#     if anime_id in Animes:
#         abort(409, message="Anime {} already exists".format(anime_id))

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'anime_url': fields.String
}


class Welcome(Resource):
    def get(self):
        return make_response(render_template('index.html'))


class Anime(Resource):
    @marshal_with(resource_fields)
    def get(self,anime_id):
        result = AnimeModel.query.filter_by(id=anime_id).first()
        if not result:
            abort(404,message="Opps! Could not Find")
        return result
   
    @marshal_with(resource_fields)
    def put(self,anime_id):
        args = anime_put_args.parse_args()
        result = AnimeModel.query.filter_by(id=anime_id).first()
        if result:
            abort(409,message="Anime already exists")
        anime = AnimeModel(id=anime_id,name=args['title'],description=args['description'],anime_url=args['image_url'])
        db.session.add(anime)
        db.session.commit()
        return anime, 201
    
    def delete(self,anime_id):
        result = AnimeModel.query.filter_by(id=anime_id).first()
        if not result:
            abort(404,message="Opps! Could not Find")
        db.session.delete(result)
        db.session.commit()
        return '', 204
    
#
class AnimeList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = AnimeModel.query.all()
        return result
    


class AnimeNew(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = anime_put_args.parse_args(strict=True)
        result = AnimeModel.query.all()
        arr=[]
        for res in result:
            arr.append(res.id)
        anime_id = arr[-1]+1
        anime = AnimeModel(id=anime_id,name=args['title'],description=args['description'],anime_url=args['image_url'])
        db.session.add(anime)
        db.session.commit()
        return anime, 201

api.add_resource(Anime,'/anime/<int:anime_id>')
api.add_resource(AnimeList,'/anime')
api.add_resource(AnimeNew,'/newanime')
api.add_resource(Welcome,'/')

if __name__ == '__main__':
    app.run(debug=True)