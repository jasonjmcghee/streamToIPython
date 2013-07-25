import cv2, cv
import numpy as np

# create video capture
cap = cv2.VideoCapture(0)
video  = cv2.VideoWriter('video.mp4', cv.CV_FOURCC('x', '2', '6','4'), 25, (640, 480))

while True:

    _,frame = cap.read() # read the frames

    frame = cv2.blur(frame,(3,3)) # smooth it

    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv,np.array((0, 150, 0)), np.array((3, 255, 255))) # 0-180, 0-255, 0-255
    thresh2 = thresh.copy()

    # find contours in the threshold image
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE) # var hierarchy

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(frame,(cx,cy),5,(0, 255, 0))

    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('frame',frame)
    video.write(frame) # save to file
    #cv2.imshow('thresh',thresh2)
    if cv2.waitKey(33)== 113:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
video.release()
cap.release()

