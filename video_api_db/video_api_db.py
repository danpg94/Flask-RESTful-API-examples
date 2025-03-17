# A simple example API for storing video metadata in order to familiarize myself with 
# the Flask RESTful library

# NOTE: make sure to install packages in requirements.txt in a virtual enviornment
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from os import path

# Creating the Flask app and the Flask RESTful api object
app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name {self.name}, views = {self.views}, likes = {self.likes})"

if not path.isfile("database.db"):
    db.create_all()

# Parser for defining the valid values for the API, only video "name" is required
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")

# 
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
} 

# Defining the methods for the video metadata API (GET, PUT, DELETE) 
class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result: 
            abort(409, message="Video id taken...")
        video = VideoModel(id = video_id, 
                           name=args['name'], 
                           views=args['views'], 
                           likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Video id not found")
        if args['name']:
            result.name = args["name"]
        if args['views']:
            result.views = args["views"]
        if args['likes']:
            result.likes = args["likes"]
        db.session.commit()
        return result, 201

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Video id not found")
        db.session.delete(result)
        db.session.commit()
        return 'video deleted', 204
        

# Add the API to the Flask app
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)