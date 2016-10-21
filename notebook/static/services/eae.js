define([
    'base/js/utils',
    ],
function(utils) {
    "use strict";

    var Eae = function(options) {
		this.eae_url = "146.169.15.140:8081";
		this.base_url = options.base_url;
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
		console.log("List Clusters");

		var settings = {
            type : "GET"
        };
        var url = this.api_eae("EAEManagement/retrieveClusters");
		
		return utils.promising_ajax(url, settings);
	};
	
	Eae.prototype.Submit = function(submit_data) {
		console.log("Eae Submit:");
		console.log(submit_data);
		var payload = submit_data;
		var settings = {
            type : "POST",
			processData: false,
            data: JSON.stringify(payload),
            dataType: "json",
            contentType: 'application/json',
        };
        var url = this.api_eae("submit");
        return utils.promising_ajax(url, settings);
    };
	
	Eae.prototype.PreSubmit = function(submit_data) {
		console.log("Eae PreSubmit:");
		console.log(submit_data);
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