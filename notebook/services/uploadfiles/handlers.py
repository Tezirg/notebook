import uuid

import os
import tornado
from tornado import web, gen
from urllib import unquote

from ...base.handlers import APIHandler, json_errors

SECRET_KEY = 'hard to guess string'
UPLOAD_FOLDER = '/home/eae/jupyter/'
THUMBNAIL_FOLDER = 'thumbnail/'
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg', 'jpeg', 'bmp', 'rar', 'zip', '7zip', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@web.stream_request_body
class UploadFilesHandler(APIHandler):
    def initialize(self):
        self.bytes_read = 0

    def data_received(self, chunk):
        self.bytes_read += len(chunk)

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
        self.finish(filename + " is uploaded!! Check %s folder" % UPLOAD_FOLDER)

        return 200

    @web.authenticated
    @json_errors
    @gen.coroutine
    def put(self):
        print self.request
        print self.request.headers
        filename = "toto.txt"
        mtype = self.request.headers.get('Content-Type')
        print 'PUT "%s" "%s" %d bytes', filename, mtype, self.bytes_read
        with open(UPLOAD_FOLDER + filename, 'a') as f:
            f.write(self.request.body)
            f.close()
        self.write('OK')
        return 200


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------

default_handlers = [
    (r"/api/uploadfiles", UploadFilesHandler)

]
