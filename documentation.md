# Documentation

Document your design decisions and building process here!

# Documentation

## Building the box

For this assignment we used the following things given to us by our master:
- cardboard box (bottom flaps closed, top flaps open)
- Intel RealSense D435
- Acrylic Plate

Since normal tape couldn't secure the camera enough inside of the box, we decided to 3D print a camera holder. It's made out of TPU filament and is secured with tape on the botto of the cardboard box. The acrylic plate is put on top of the box, where 2 flaps are taped to the outside and two tapes indicate where the acrylic tape needs to be put. On the plate we also taped a DIN-A4 paper sheet with a drawn rectangle showing the size of the captured image of the camera.

![3d printed camera cage](/assets/camera_holder.jpeg)

With this we made sure that the box can be set up the same every usage.

TODO: some nice pictures and some nicer text

## Code

We tried out two approaches:
1. CNN
2. Hard Coded Threshholds

In the end we decided to go with the second plan, but had already put in work in plan one. Because of this we want to explain shortly what we did, so we didn't do it completely unnecessary. 
We captured 7783 samples (=photos of fingers) for trainingsdata, labeled with either "hover" or "touch". For this we detected the bounding box of the fingers and added padding to it, so the box for capturing was always the same size. We trained a CNN with this data, which we called Erwin ("ein richtig wildes input netzwerk"). For the first few tries it worked relatively good, but with progress in code and assignment tasks we found out that this will not be the way. Finally, we went back to hard coded threshholds, which can be seen in the code.

## Usage Guide

1. Set up the Box
    - tape the flaps as following (pictures)
2. Connect the camera
3. Check if camera ID is the same as in the code 
4. Start `touch.py` 
5. Press `s` to calibrate the camera to the light
6. Start whatever application you want
7. Give us many points


