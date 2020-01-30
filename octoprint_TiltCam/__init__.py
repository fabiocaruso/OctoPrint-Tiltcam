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
                    octoprint.plugin.SimpleApiPlugin):

        def on_after_startup(self):
                self.refPoint = [1200, 1200]
                self.RANGE_X = [600, 1600]
                self.RANGE_Y = [600, 1600]

                self._logger.info(self._connectivity_checker.host)

                self.pi = pigpio.pi()
                # TODO: Save last state of pulsewidth and set it here as startpoint
                #self.pi.set_servo_pulsewidth(2, 1200)
                #self.pi.set_servo_pulsewidth(3, 1200)
                self._logger.info("Hello World!" + str(self._settings.get(["xgpio"])))

	##~~ SimpleApiPlugin mixin

        def get_api_commands(self):
                return dict(
                    move=["x", "y"],
                    setRefPoint=[]
                )
        
        def on_api_command(self, command, data):
                gpioX = int(self._settings.get(["xgpio"]))
                gpioY = int(self._settings.get(["ygpio"]))
                if command == "move":
                        stepX = (self.RANGE_X[1] - self.RANGE_X[0]) * data["x"]
                        stepY = (self.RANGE_Y[1] - self.RANGE_Y[0]) * data["y"]
                        self.pi.set_servo_pulsewidth(gpioX, self.refPoint[0] + stepX)
                        self.pi.set_servo_pulsewidth(gpioY, self.refPoint[1] + stepY)
                elif command == "setRefPoint":
                        currentX = self.pi.get_servo_pulsewidth(gpioX)
                        currentY = self.pi.get_servo_pulsewidth(gpioY)
                        self.refPoint = [currentX, currentY]
                    
        def on_api_get(self, request):
                return flask.jsonify(foo="bar")

        ##~~ SettingsPlugin mixin

        def get_settings_defaults(self):
            return dict(
                xgpio="3",
                ygpio="2",
                vid="url"
            )

        def get_template_vars(self):
            return dict(
                    xgpio=self._settings.get(["xgpio"]),
                    ygpio=self._settings.get(["ygpio"]),
                    vid=self._settings.get(["vid"])
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
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
        global __plugin_implementation__
        __plugin_implementation__ = TiltcamPlugin()

        global __plugin_hooks__
        __plugin_hooks__ = {
                "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
        }

