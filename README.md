# LabProj-G16
<pre>
- Chen Weizhuang, Bernie	  Bcwz		    1901850@sit.singaporetech.edu.sg		

- Choong Jia Jun		  joecjj            1901837@sit.singaporetech.edu.sg

- Shaun Yam Zhan Hui	 	  cardstriker	    1901871@sit.singaporetech.edu.sg

- Stuart Theodore Koh Wen You	  Exolotl 	    1901875@sit.singaporetech.edu.sg

- Tan Yi Kang 			  xiujk71	    1901879@sit.singaporetech.edu.sg
</pre>

## Smart Wristband with Fall Detection
A raspberry pi project that is capable of tracking the user’s heart rate and movements to differentiate between different activities that the user is doing .

## Motivation
In hospitals, where heart rate monitors are considered critical, its functionality is increased through the use of external wires and sensors to alert medical staff in case of an emergency.
For more mobile patients, this might be more difficult as this set-up is tedious to carry around.
A possible solution is to create a wristband that can measure pulse and fall detection.

## Usage
![alt text](https://github.com/UOG-AY20-CSC2003/LabProj-G16/blob/master/Image/raspi_system_architecture.png)
<br>
This setup will require three different RPi which will all be connected to a local hotspot network, one pioneer600 module and Thingsboard to visualise the data collected from MPU6050 and MAX30100 sensors.<br>
Copy the MAX30100_code folder into the buzzer RPi and run the buzzer.py <br>
Copy the MAX30100_code folder into the Heart Rate RPi and run the heart_rate.py <br>
Copy the MPU6050_code folder into the Main RPi and run main.py

## Training Code
"keras-train.py" is the code used to train the model, to be used on a PC.
"dataset.csv" is the dataset we have used to train the model.

## Models Trained
"testmodel-new-C-24x24" is the model we will be using for our project.
The other models, "testmodel-new-C-12", "testmodel-new-C-12x12" and "testmodel-new-C-24", were used for comparison testing, and not used in the final version.
