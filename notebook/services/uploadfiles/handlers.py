import uuid

import os
from tornado import web, gen

from ...base.handlers import APIHandler, json_errors

SECRET_KEY = 'hard to guess string'
UPLOAD_FOLDER = '/home/eae/jupyter/'
THUMBNAIL_FOLDER = 'thumbnail/'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])

def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


class UploadFilesHandler(APIHandler):

    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self):
        print "I am in the post"
        # files = request.files['file']
        #
        # if files:
        #     filename = secure_filename(files.filename)
        #     filename = gen_file_name(filename)
        #     mime_type = files.content_type
        #
        #     if not allowed_file(files.filename):
        #         result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")
        #
        #     else:
        #         # save file to disk
        #         uploaded_file_path = os.path.join(UPLOAD_FOLDER, filename)
        #         files.save(uploaded_file_path)
        #
        #         # create thumbnail after saving
        #         if mime_type.startswith('image'):
        #             create_thumbnail(filename)
        #
        #         # get file size after saving
        #         size = os.path.getsize(uploaded_file_path)
        #
        #         # return json for js call back
        #         result = uploadfile(name=filename, type=mime_type, size=size)
        #
        #     simplejson.dumps({"files": [result.get_file()]})
        return 200

    @web.authenticated
    @json_errors
    @gen.coroutine
    def post(self):
        print "I am in the post"
        file = self.request.files['file[0]'][0]
        filename = file['filename']
        with open(UPLOAD_FOLDER + filename, 'a') as f:
            f.write(str(file['body']))
            f.close()
        self.finish(filename + " is uploaded!! Check %s folder" %UPLOAD_FOLDER)

        return 200


    #
    # def get_file(self, filename):
    #     return send_from_directory(os.path.join(UPLOAD_FOLDER), filename=filename)


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------

default_handlers = [
    (r"/api/uploadfiles", UploadFilesHandler)

]