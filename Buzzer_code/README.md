## Installation for Pioneer600
In order to run the following code, the following packages has to be installed on raspberry pi.<br><br>
Install Wiring Pi Library:
<pre>
cd
sudo apt-get install wiringpi
gpio -v
</pre>
<br>
Install Python 3:
<pre>
cd
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install RPi.GPIO
</pre>
<br>
Install Python Library for buzzer RPi
<pre>
sudo pip3 install pillow
sudo pip3 install numpy
sudo apt-get install libopenjp2-7
sudo apt install libtiff
sudo apt install libtiff5
sudo apt-get install libatlas-base-dev
</pre>
<br>

## Running the buzzer program
Start the buzzer program and wait for signal from main.py