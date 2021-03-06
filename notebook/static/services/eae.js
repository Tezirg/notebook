define([
    'base/js/utils',
    ],
function(utils) {
    "use strict";

    var Eae = function(options) {
		this.eae_url = "localhost:8081";
		this.base_ip = "localhost";
		this.base_url = options.base_url;
        this.ssh_port = 22;
        this.host_ip = "127.0.0.1";

		var that = this;
		options.config.loaded.then(function() {
		    console.log("Config loaded:");
		    console.log(options.config.data);
		    if (options.config.data.hasOwnProperty('eae_ip') && options.config.data.hasOwnProperty('eae_port')) {
                that.eae_url = options.config.data['eae_ip'] + ":" + options.config.data['eae_port'].toString();
                that.ssh_port = options.config.data['eae_host_ssh_port'];
                that.host_ip = options.config.data['eae_host_ip'];
            }
		});
		options.config.load();
    };
	
	Eae.prototype.api_eae = function() {
		var url_parts = [
            this.eae_url, 'interfaceEAE/', 
			utils.url_join_encode.apply(null, arguments)
        ];
        return "https://" + utils.url_path_join.apply(null, url_parts);
	}
	Eae.prototype.api_notebook = function() {
        var url_parts = [
            this.base_url, 'api/eae',
            utils.url_join_encode.apply(null, arguments),
        ];
        return utils.url_path_join.apply(null, url_parts);
    };
	
	Eae.prototype.isAlive = function () {
        var settings = {
            type : "GET"
        };
        var url = this.api_eae("utilities/isAlive");
		console.log(url);
        return utils.promising_ajax(url, settings);
    };
	
	Eae.prototype.listClusters = function () {
		var settings = {
            type : "GET"
        };
        var url = this.api_eae("EAEManagement/retrieveClusters");
		
		return utils.promising_ajax(url, settings);
	};
	
	Eae.prototype.Submit = function(submit_data) {
		var payload = submit_data;
		payload['host_ip'] = this.host_ip;
		payload['ssh_port'] = this.ssh_port;
		var settings = {
            type : "POST",
			processData: false,
            data: JSON.stringify(payload),
            contentType: 'application/json'
        };
        var url = this.api_eae("OpenLava/submitJob");
        return utils.promising_ajax(url, settings);
    };
	
	Eae.prototype.PreSubmit = function(submit_data) {
		var payload = submit_data;
		var settings = {
            type : "POST",
			processData: false,
            data: JSON.stringify(payload),
            contentType: 'application/json',
            dataType : "json"
        };
		var url = this.api_notebook("submit");
        return utils.promising_ajax(url, settings);
	};
	
	return { Eae: Eae };
});