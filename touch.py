import cv2
import sys
import numpy as np
import time


video_id = 6
running = False
threshold = 75


if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

cap = cv2.VideoCapture(video_id)



def process_img(frame, window_w, window_h):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    img_contours = cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)

    for ctn in contours:
        if 200 < cv2.contourArea(contour=ctn) < 3500:
            x,y,w,h = cv2.boundingRect(ctn)
            if (x > window_w - 50 or x < 50 or y > window_h - 50 or y < 50):
                break
            M = cv2.moments(ctn)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(img_contours, (cX, cY), 7, (255, 255, 255), -1)
            cv2.rectangle(img_contours,(cX-50, cY-50),(cX+50, cY+50),(0, 0, 255),2)
            cv2.rectangle(img_contours,(x,y),(x+w,y+h),(0,255,0),2)

            cut = frame[cY-50:cY+50, cX-50:cX+50]
            #resized = cv2.resize(cut, (100, 100))
            title = f'{time.time()}-hover-s.png'
            cv2.imwrite(f'hover-data-border-test/{title}', cut)

    return img_contours



while True:
    # Capture a frame from the webcam
    ret, frame = cap.read() # ret = return wenn bild abkackt gibt das False
    WINDOW_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    WINDOW_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if not running:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        threshold = np.bincount(img_gray.flatten()).argmax() / 2
    else:
        img = process_img(frame, WINDOW_WIDTH, WINDOW_HEIGHT)
    cv2.imshow('frame', img)

    # Wait for a key press and check if it's the 'q' key
    # timeout in () -> returned Keycode == q
    if cv2.waitKey(1) & 0xFF == ord('s'):
        running = True
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()