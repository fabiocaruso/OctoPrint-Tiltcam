# coding=utf-8
from __future__ import absolute_import
import flask, pigpio

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class TiltcamPlugin(octoprint.plugin.StartupPlugin,
                    octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.SimpleApiPlugin,
                    octoprint.plugin.WizardPlugin):

        def on_settings_initialized(self):
                self.status = ""
                self.RANGE_X = [self._settings.get_int(["xRangeMin"]), self._settings.get_int(["xRangeMax"])]
                self.RANGE_Y = [self._settings.get_int(["yRangeMin"]), self._settings.get_int(["yRangeMax"])]
                refx = self._settings.get_int(["xstart"]) + self.RANGE_X[0]
                refy = self._settings.get_int(["ystart"]) + self.RANGE_Y[0]
                lastx = self._settings.get_int(["xlast"])
                lasty = self._settings.get_int(["ylast"])
                if (lastx is not None) and (lasty is not None) and (self._settings.get_boolean(["startingPoint"]) == False):
                    refx = lastx
                    refy = lasty
                self.refPoint = [refx, refy]
                self.pi = pigpio.pi()
                try:
                    self.pi.set_servo_pulsewidth(self._settings.get_int(["xgpio"]), refx)
                    self.pi.set_servo_pulsewidth(self._settings.get_int(["ygpio"]), refy)
                except:
                    self.status = "Pigpiod is not running!<br/>Please follow these <a href='https://github.com/fabiocaruso/OctoPrint-Tiltcam/blob/master/docs/pigpiod_installation.md'>instuctions</a> to setup."

        ##~~ WizardPlugin mixin

        def is_wizard_required(self):
                return (self._settings.get(["xgpio"]) is None) or (self._settings.get(["ygpio"]) is None)

        def get_wizard_version(self):
                return 1

	##~~ SimpleApiPlugin mixin

        def get_api_commands(self):
                return dict(
                    move=["x", "y"],
                    setRefPoint=[],
                    setLastPoint=[]
                )
        
        def on_api_command(self, command, data):
                if self.status != "":
                    return flask.jsonify(result=self.status)
                gpioX = self._settings.get_int(["xgpio"])
                gpioY = self._settings.get_int(["ygpio"])
                if command == "move":
                        stepX = (self.RANGE_X[1] - self.RANGE_X[0]) * data["x"]
                        stepY = (self.RANGE_Y[1] - self.RANGE_Y[0]) * data["y"]
                        abX = self.refPoint[0] + stepX
                        abY = self.refPoint[1] + stepY
                        if self.RANGE_X[0] <= abX <= self.RANGE_X[1] and self.RANGE_Y[0] <= abY <= self.RANGE_Y[1]:
                            self.pi.set_servo_pulsewidth(gpioX, abX)
                            self.pi.set_servo_pulsewidth(gpioY, abY)
                elif command == "setRefPoint":
                        currentX = self.pi.get_servo_pulsewidth(gpioX)
                        currentY = self.pi.get_servo_pulsewidth(gpioY)
                        self.refPoint = [currentX, currentY]
                elif command == "setLastPoint":
                        currentX = self.pi.get_servo_pulsewidth(gpioX)
                        currentY = self.pi.get_servo_pulsewidth(gpioY)
                        self._settings.set_int(["xlast"], currentX)
                        self._settings.set_int(["ylast"], currentY)
                        self._settings.save()
                    
        def on_api_get(self, request):
                return flask.jsonify(foo="bar")

        ##~~ SettingsPlugin mixin

        def get_settings_defaults(self):
            return dict(
                xgpio=None,
                ygpio=None,
                startingPoint=True,
                xstart=600,
                ystart=600,
                xRangeMin=500,
                xRangeMax=2500,
                yRangeMin=500,
                yRangeMax=2500,
                xlast=None,
                ylast=None
            )

        def get_template_vars(self):
            return dict(
                    xgpio=self._settings.get(["xgpio"]),
                    ygpio=self._settings.get(["ygpio"]),
                    startingPoint=self._settings.get(["startingPoint"]),
                    xstart=self._settings.get(["xstart"]),
                    ystart=self._settings.get(["ystart"]),
                    xRangeMin=self._settings.get(["xRangeMin"]),
                    xRangeMax=self._settings.get(["xRangeMax"]),
                    yRangeMin=self._settings.get(["yRangeMin"]),
                    yRangeMax=self._settings.get(["yRangeMax"]),
                    status=self.status
            )

        ##~~ AssetPlugin mixin

        def get_assets(self):
            # Define your plugin's asset files to automatically include in the
            # core UI here.
            return dict(
                    js=["js/TiltCam.js"],
                    css=["css/TiltCam.css"],
                    less=["less/TiltCam.less"]
            )

        ##~~ Softwareupdate hook

        def get_update_information(self):
            # Define the configuration for your plugin to use with the Software Update
            # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
            # for details.
            return dict(
                    TiltCam=dict(
                        displayName="Tiltcam Plugin",
                        displayVersion=self._plugin_version,

                        # version check: github repository
                        type="github_release",
                        user="fabiocaruso",
                        repo="OctoPrint-Tiltcam",
                        current=self._plugin_version,

                        # update method: pip
                        pip="https://github.com/fabiocaruso/OctoPrint-Tiltcam/archive/{target_version}.zip"
                    )
            )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Tiltcam Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
        global __plugin_implementation__
        __plugin_implementation__ = TiltcamPlugin()

        global __plugin_hooks__
        __plugin_hooks__ = {
                "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
        }

