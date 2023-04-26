from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "you entered invalid image please check extension"
    }

    def _deserialize(self, value, __, _) -> FileStorage:
        if value is None:
            return None
        if not isinstance(value, FileStorage):
            self.fail("invalid")
        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)
