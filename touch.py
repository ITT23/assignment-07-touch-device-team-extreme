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



def process_img(frame):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    img_contours = cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)

    for ctn in contours:
        if 400 < cv2.contourArea(contour=ctn) < 2500:
            x,y,w,h = cv2.boundingRect(ctn)
            cv2.rectangle(img_contours,(x,y),(x+w,y+h),(0,255,0),2)
            cut = frame[y:y+h, x:x+w]
            resized = cv2.resize(cut, (36, 36))
            title = f'{time.time()}-touch-a.png'
            cv2.imwrite(f'touch-data/{title}', resized)

    return img_contours



while True:
    # Capture a frame from the webcam
    ret, frame = cap.read() # ret = return wenn bild abkackt gibt das False

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if not running:
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        threshold = np.bincount(img_gray.flatten()).argmax() - 45
    else:
        img = process_img(frame)
    cv2.imshow('frame', img)

    # Wait for a key press and check if it's the 'q' key
    # timeout in () -> returned Keycode == q
    if cv2.waitKey(1) & 0xFF == ord('s'):
        running = True
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()