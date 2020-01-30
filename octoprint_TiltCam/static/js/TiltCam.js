/*
 * View model for OctoPrint-Tiltcam
 *
 * Author: Fabio Caruso
 * License: MIT
 */
$(function() {
    function TiltcamViewModel(parameters) {
        var self = this;
	var refPoint = {X: -1, Y: -1};
	var cview = document.getElementById("cview");
	var host = location.protocol + "//" + window.location.host;

        // assign the injected parameters, e.g.:
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];

	self.x = ko.observable();
	self.y = ko.observable();
	self.bgImage = ko.observable();
	
	function throttle(callback, interval) {
		let enableCall = true;
		return function(...args) {
			if (!enableCall) return;
			enableCall = false;
			callback.apply(this, args);
			setTimeout(() => enableCall = true, interval);
		}
	}
	
	function sendData(data) {
		var xhr = new XMLHttpRequest();
		var url = "/api/plugin/TiltCam";
		xhr.open("POST", url, true);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.setRequestHeader("X-Api-Key", this.settings.api.key());
		xhr.onreadystatechange = function () {
			if (xhr.readyState === 4 && xhr.status === 200) {
				var json = JSON.parse(xhr.responseText);
				console.log("worked");
			}
		};
		xhr.send(JSON.stringify(data));
	}

	self.onBeforeBinding = function() {
		self.settings = self.settingsViewModel.settings;
		console.log(self.settings.api.key());
	};
	
	//console.log("URL: " + self.settings.webcam.streamUrl())
	self.bgImage = 'url(' + host + '/webcam/?action=stream)';
	
	self.cviewmm = throttle(function(data, ev) {
		var offPoint = {X: ev.offsetX - refPoint.X, Y: refPoint.Y - ev.offsetY};
		if (refPoint.X != -1 && refPoint.Y != -1) {
			var data = {
				"command": "move",
				"x": offPoint.X.toString() / cview.clientWidth,
				"y": offPoint.Y.toString() / cview.clientHeight
			};
			sendData(data);
		}
		self.x(ev.offsetX - refPoint.X);
		self.y(refPoint.Y - ev.offsetY);
	}, 50);

	self.cviewmd = function(data, ev) {
		refPoint.X = ev.offsetX;
		refPoint.Y = ev.offsetY;
		var data = {
			"command": "setRefPoint",
		};
		sendData(data);
	};

	self.cviewmu = function(data, ev) {
		refPoint.X = -1;
		refPoint.Y = -1;
	};

    };

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: TiltcamViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["loginStateViewModel", "settingsViewModel"],
        // Elements to bind to, e.g. #settings_plugin_TiltCam, #tab_plugin_TiltCam, ...
        elements: ["#tab_plugin_TiltCam"]
    });
});
