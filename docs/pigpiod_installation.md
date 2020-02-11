# Installing pigpiod

1. Get putty from [this](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) site and install it.
2. Open putty, type 'octopi.local' in the 'Host Name' field and press 'Open'.
3. A black window appears. Type the username 'pi' and the default password (should be 'raspberry').
4. If the welcome message of octoprint appears, you are logged in successfully. Now Type ```sudo apt-get update```
5. You'll be asked to enter a password. Type the same password from 3.
6. If the command executed without any errors you can type ```sudo apt-get install pigpio```. Agree the installation with 'y'.
7. Now you should be able to run pigpiod with the following command ```sudo pigpiod```
8. Reboot your pi with ```sudo reboot```
9. Done!
