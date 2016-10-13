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
		console.log("Eae IsAlive:");
        var settings = {
            type : "GET"
        };
        var url = this.api_eae("utilities/isAlive");
		console.log(url);
        return utils.promising_ajax(url, settings);
    };
	
	Eae.prototype.Submit = function(submit_data) {
		console.log("Eae Submit:");
		console.log(submit_data);
		var settings = {
            type : "POST",
            data : submit_data,
            dataType: "json",
            contentType: 'application/json',
        };
        var url = this.api_eae("submit");
        return utils.promising_ajax(url, settings);
    };
	
	Eae.prototype.PreSubmit = function(data) {
		console.log("Eae PreSubmit:");
		console.log(data);
		var settings = {
            processData : false,
            type : "POST",
            data: data,
            contentType: 'application/json',
            dataType : "json",
        };
        return utils.promising_ajax(this.api_notebook("submit"), settings);
	};
	
	return { Eae: Eae };
});