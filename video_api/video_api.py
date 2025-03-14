# A simple example API for storing video metadata in order to familiarize myself with 
# the Flask RESTful library

# NOTE: make sure to install packages in requirements.txt in a virtual enviornment
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

# Creating the Flask app and the Flask RESTful api object
app = Flask(__name__)
api = Api(app)

# Parser for defining the valid values for the API, only video "name" is required
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video")
video_put_args.add_argument("likes", type=int, help="Likes of the video")

# Video metadata "database" checkers
videos = {}

def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Could not find video...")

def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID...")

# Defining the methods for the video metadata API (GET, PUT, DELETE) 
class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]
    
    def put(self, video_id):
        abort_if_video_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204

# Add the API to the Flask app
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)