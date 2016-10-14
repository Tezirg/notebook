import json

from tornado import gen, web

from ...base.handlers import APIHandler, json_errors
from ...nbconvert.handlers import get_exporter
from jupyter_client.jsonutil import date_default
from notebook.utils import url_path_join, url_escape

class EaeHandler(APIHandler):

    @web.authenticated
    @json_errors
    @gen.coroutine
    def post(self):
		"""Eae submit query prep. From notebook data form
		
		POST /api/eae/submit
		"""

		data = self.get_json_body();
		print(data);
		
		exporter = get_exporter("script");
		print("Got the script exporter");
		scripts = []
		for f in data['files']:
			if f.rfind(".ipynb") != -1:
				model = self.contents_manager.get(path=f)
				scripts.append(exporter.from_notebook_node(model['content']));
		print(scripts);
		
		self.set_status(200);
		self.set_header('Content-Type', 'application/json');
		self.finish(json.dumps({ "test" : True }, default=date_default));
		
#-----------------------------------------------------------------------------
# URL to handler mappings
#-----------------------------------------------------------------------------

default_handlers = [
    (r"/api/eae/submit", EaeHandler)
]
