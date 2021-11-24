# dataCollectorApp
<hr>
Data Collection app for kivy 
<br>


## Features
Following is what the app does:
- Take data from each and every sensor on the phone ( you have to give access to the app on first start) and display it on a material ui screen
- Save the data into a csv file in the downlaods folder.

<br>


## How to Build and notes:
 On the first run, you must allow permission to access downloads folder. after which a csv file with the name values.csv will appear in the downloads folder.The code is pretty straightforward so do feel free to build your own version with [the colab link provided](https://gist.github.com/nandanhere/5ba4d76cad282a0c0b64a1ec1b8530e1). This is the same link as the Kivytimetable app and mostly does the same job.
 
 
 
To See the adb runtime log use the command 

     adb logcat -s Datacollectorservice:V python:V
 