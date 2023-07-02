# Documentation

**Team Extreme: Tina Emmert & Sabrina Hößl**

Things used for this assignment:

- cardboard box
- Intel RealSense D435
- Acrylic Plate
- Paper
- 3D printed camera holder

## Building the box 

We build the box with the bottom closed, top opend. One of the flaps of the box is taped to the side and the other flaps are used to hold the acrylic plate in place. We marked the spot for the acrylic plate with green maker. On top of the plate we taped paper as a diffusor. A drawn rectangle shows what part of the paper is captured by the camera. Since normal tape couldn't hold the camera enough inside the box, we decided to quickly 3D print a camera holder. It's made out of TPU filament and taped to the bottom of the box. We also cut a hole in the box to put the USB cable through.

![3d printed camera cage](/assets/camera_holder.jpeg)

## Code

We tried out two approaches:

1. CNN
2. Hard Coded Threshholds

In the end we decided to go with the second plan, but had already put in lot of work in the CNN plan. Because of this we want to explain shortly what we did, so we didn't do it completely unnecessary.
We captured 7783 samples (=photos of fingers) for trainingsdata, labeled with either "hover" or "touch". For this we detected the bounding box of the fingers and added padding to it, so the box for capturing was always the same size. We trained a CNN with this data, which we called ERWIN ("ein richtig wildes input netzwerk"). With progress in code and assignment tasks the output was not good enough, so we had so retire ERWIN (but kept him in an extra branche `erwin-legacy`) and do it with thresholds.

For this we transform the frame to greyscale picture and perform a binary threshold. Detected objects (black) are drawn with a contour, which we select by the area inside the contour to make sure palm or other big object are not tracked.


## Usage Guide

1. Set up the Box
2. Connect the camera
3. Check if camera ID is the same as in the code
4. Turn on some lights (please don't be a Gollum)
5. Start `touch-input.py` (optional: input params video_id and receiver ip)
6. Press `s` to calibrate the camera to the light (do not place anything on the touchscreen yet)
7. Hover by light touching the surface with your fingertip, Touch by stronger touching the surface and bending the finger a bit
8. Start whatever application you want
9. Give us many points
