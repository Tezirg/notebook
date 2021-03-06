import json
import pprint
import io
import os
import stat
import zipfile
import re

from subprocess import call
from tornado import gen, web

from ...base.handlers import APIHandler, json_errors
from ...nbconvert.handlers import get_exporter
from jupyter_client.jsonutil import date_default
# from notebook.utils import url_path_join, url_escape


class EaeHandler(APIHandler):
    exporter = get_exporter("script")

    @web.authenticated
    @json_errors
    @gen.coroutine
    def post(self):
        """Eae submit query prep. From notebook data form

        POST /api/eae/submit
        """

        data = self.get_json_body()

        to_zip = []
        mainScript = ""
        scripts = []
        files = []

        # Handle main script
        model = self.contents_manager.get(path=data['mainScriptPath'])
        to_zip += self._dataExtract(model)
        mainScript = to_zip[-1]['filename']

        # Handle other scripts
        for f in data['scriptsPath']:
            model = self.contents_manager.get(path=f)
            to_zip += self._dataExtract(model)
            scripts.append(to_zip[-1]['filename'])

        # Handle other files & dirs
        # for f in data['filesPath']:
            # model = self.contents_manager.get(path=f)
            # extract = self._dataExtract(model)
            # for e in extract:
            #     files.append(e['filename'])
            # to_zip += extract

        # Prepare the zip file
        zip_path = "/tmp/" + data['id'] + '.zip'
        zipf = zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_STORED,allowZip64 = True)
        for entry in to_zip:
            zipf.writestr(entry['filename'], entry['content'])
        zipf.close()

        # Handle other files & dirs
        for f in data['filesPath']:
            zipCommand = "zip -r -u -0 " + zip_path + " " + f
            print zipCommand
            call([zipCommand], shell=True)

        # Chmod 666 the zip file so it can be accessed
        os.chmod(zip_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

        self.set_status(200)
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(
            {"id": data['id'], "zip": zip_path, "mainScriptExport": mainScript, "scriptsExport": scripts,
             "filesExport": files}, default=date_default))
        return

    def _dataExtract(self, model):
        """Extract contents from file model
        Formats name, export script and recurs into directories
        """

        data = []
        if model['type'] == 'file' and model['content'] != None:
            data.append({"filename": model['name'], "content": model['content']})
        elif model['type'] == 'notebook' and model['content'] != None:
            output, ressources = self.exporter.from_notebook_node(model['content'])
            name = model['name'] + ressources['output_extension']
            data.append({"content": output, "filename": name})
            r1 = re.sub(r'#(.*SparkConf\(\).*)', r'\1', data[-1]['content'], flags=re.MULTILINE)
            r2 = re.sub(r'#(.*SparkContext\(.*\).*)', r'\1', r1, flags=re.MULTILINE)
            data[-1]['content'] = r2
        elif model['type'] == 'directory' and model['content'] != None:
            for file in model['content']:
                root = file['path'].split('/')[1:-1]
                root = "/".join(root)
                f = self.contents_manager.get(path=file['path'])
                content = self._dataExtract(f)
                if content:
                    for c in content:
                        if file['type'] != 'directory':
                            c['filename'] = root + "/" + c['filename']
                    data += content
        return data


# -----------------------------------------------------------------------------
# URL to handler mappings
# -----------------------------------------------------------------------------

default_handlers = [
    (r"/api/eae/submit", EaeHandler)
]

