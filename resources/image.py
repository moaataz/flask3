from libs import image_helper
from flask_restful import request, Resource
from flask import send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_uploads import UploadNotAllowed
import os
import traceback

from schemas.image import ImageSchema

image_schema = ImageSchema()


class UploadImage(Resource):
    @jwt_required()
    def post(self):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = image_helper.save_image(data["image"], folder)
            basename = image_helper.get_basename(image_path)
            return {"message": f'image "{basename}" is uploaded successfully'}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {
                "message": f"image extension '{extension}' is not allowed please try another image"
            }, 400


class Image(Resource):
    @jwt_required()
    def get(self, filename):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_safe(filename):
            return {"message": f"image has illegal file name '{filename}'"}, 400
        try:
            return send_file(image_helper.get_path(filename, folder=folder))
        except FileNotFoundError:
            return {"message": f"file with name '{filename}' is not exists"}, 404

    @jwt_required()
    def delete(self, filename):
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        if not image_helper.is_filename_safe(filename):
            return {"message": f"image has illegal file name '{filename}'"}, 400
        try:
            os.remove(image_helper.get_path(filename, folder=folder))
            return {"message": f"image with name {filename} deleted successfully"}, 201
        except FileNotFoundError:
            return {"message": f"file with name '{filename}' is not exists"}, 404
        except:
            return {"message": "an error occured please try again later"}, 500
