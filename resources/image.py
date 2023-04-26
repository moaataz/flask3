from libs import image_helper
from flask_restful import request, Resource
from flask import send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_uploads import UploadNotAllowed

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
