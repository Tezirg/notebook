import json
import pprint
import io
import os
import stat
import zipfile
import re
import socket
import urlparse

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

		hostname = urlparse.urlparse("%s://%s" % (self.request.protocol, self.request.host)).hostname;
		ip_address = socket.gethostbyname(hostname);
		
		data = self.get_json_body();		
		exporter = get_exporter("script");

		to_zip = [];
		scripts = [];
		mainScript = "";
		
		model = self.contents_manager.get(path=data['mainScriptPath']);
		output, ressources = exporter.from_notebook_node(model['content']);
		
		root, ext = os.path.splitext(model['name']);
		name = root + ressources['output_extension'];
		mainScript = name;
		to_zip.append({ "content": output, "filename": mainScript });
		if data['clusterType'] == 'Spark' :
			r1 = re.sub(r'#(.*SparkConf\(\).*)', r'\1', to_zip[-1]['content'], flags=re.MULTILINE);
			r2 = re.sub(r'#(.*SparkContext\(.*\).*)', r'\1', r1, flags=re.MULTILINE);
			to_zip[-1]['content'] = r2;
		
		for f in data['filesPath']:
				model = self.contents_manager.get(path=f);
				to_zip.append({ "filename": model['name'], "content": model['content']});
		
		for f in data['scriptsPath']:
			model = self.contents_manager.get(path=f);
			output, ressource = exporter.from_notebook_node(model['content']);
			name = os.path.splitext(model['name'])[0] + ressource['output_extension'];
			to_zip.append({ "content": output, "filename": name });
			if data['clusterType'] == 'Spark' :
					r1 = re.sub(r'#(.*SparkConf\(\).*)', r'\1', to_zip[-1]['content'], flags=re.MULTILINE);
					r2 = re.sub(r'#(.*SparkContext\(.*\).*)', r'\1', r1, flags=re.MULTILINE);
					to_zip[-1]['content'] = r2;
			scripts.append(name);
				
		

		# Prepare the zip file
		zip_path = "/tmp/" + data['id'] + '.zip';
		zipf = zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED)
		for entry in to_zip:
			zipf.writestr(entry['filename'], entry['content'])
		zipf.close();
		
		
		#Chmod 666 the zip file so it can be accessed
		os.chmod(zip_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH);
		
		self.set_status(200);
		self.set_header('Content-Type', 'application/json');
		self.finish(json.dumps({ "id": data['id'], "zip": zip_path, "mainScriptExport": mainScript, "scriptsExport": scripts, "serverIp": ip_address }, default=date_default));
		
#-----------------------------------------------------------------------------
# URL to handler mappings
#-----------------------------------------------------------------------------

default_handlers = [
    (r"/api/eae/submit", EaeHandler)
]
