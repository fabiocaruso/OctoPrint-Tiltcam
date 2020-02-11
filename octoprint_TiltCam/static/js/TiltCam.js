/*
 * View model for OctoPrint-Tiltcam
 *
 * Author: Fabio Caruso
 * License: MIT
 */
$(function() {
    function TiltcamViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];

	self.bgImage = ko.observable();

	self.refPoint = {X: -1, Y: -1};
	self.cview = document.getElementById("cview");
	self.host = location.protocol + "//" + window.location.host;
	
	self.onBeforeBinding = function() {
		self.settings = self.settingsViewModel.settings;
		self.bgImage = 'url(' + self.host + self.settings.webcam.streamUrl() + ')';
		document.getElementsByClassName("startingPoint")[0].style.display = (self.settings.plugins.TiltCam.startingPoint()) ? "block" : "none";
	};

	self.throttle = (callback, interval) => {
		let enableCall = true;
		return function(...args) {
			if (!enableCall) return;
			enableCall = false;
			callback.apply(this, args);
			setTimeout(() => enableCall = true, interval);
		}
	}
	
	self.sendData = (apikey, data) => {
		var xhr = new XMLHttpRequest();
		var url = "/api/plugin/TiltCam";
		xhr.open("POST", url, true);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.setRequestHeader("X-Api-Key", apikey);
		xhr.send(JSON.stringify(data));
	};
	
	self.cviewmm = self.throttle(function(data, ev) {
		//offPoint is the offset of the actual mouse position to the reference point
		var offPoint = {X: ev.offsetX - self.refPoint.X, Y: self.refPoint.Y - ev.offsetY};
		// If the reference point wasn't reset by a mouseup event..
		if (self.refPoint.X != -1 && self.refPoint.Y != -1) {
			// .. we can send the procentual part of the offPoint to the whole view
			var data = {
				"command": "move",
				"x": offPoint.X.toString() / self.cview.clientWidth,
				"y": offPoint.Y.toString() / self.cview.clientHeight
			};
			self.sendData(self.settings.api.key(), data);
		}
	}, 20);

	self.cviewmd = function(data, ev) {
		// Change Cursor
		ev.target.style.cursor = "grabbing";
		// Set the referencePoint to the actual point
		self.refPoint.X = ev.offsetX;
		self.refPoint.Y = ev.offsetY;
		// Trigger a reference point set on the server side
		var data = {
			"command": "setRefPoint",
		};
		self.sendData(self.settings.api.key(), data);
	};

	self.cviewmu = function(data, ev) {
		// Change Cursor
		ev.target.style.cursor = "grab";
		// Reset the referencePoint and save actual position
		self.refPoint.X = -1;
		self.refPoint.Y = -1;
		var data = {
			"command": "setLastPoint",
		};
		self.sendData(self.settings.api.key(), data);
	};

	self.startingPoint = function(data, ev) {
		elem = ev.target.parentElement.parentElement.getElementsByClassName("startingPoint")[0];
		if (elem.style.display == "none") {
			elem.style.display = "block";
		} else {
			elem.style.display = "none";
		}
		return true;
	}

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
        elements: ["#tab_plugin_TiltCam", "#settings_plugin_TiltCam", "#wizard_plugin_TiltCam"]
    });
});
