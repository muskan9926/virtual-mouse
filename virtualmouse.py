import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy


wCam, hCam = 640, 480
pTime=0
frameR=100
smothening=7
# present location and current location
plocx=0
plocy=0
clocx=0
clocy=0
# frame reduction because when we are moving upwards it is okay but we are unable to go down so setting range so thant whole screen can be used
# 0 is the id of how many cameras you have if 1 then multiple cameras
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
# to get our screen coordinates, this will gives us size of the screen
wScr,hScr =autopy.screen.size()
# print(wScr,hScr)
# 1440.0 900.0
while True:
    # 1.finding hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox =detector.findPosition(img)


    # 2. Get the tip of the index and middle fingers
    if len(lmList) !=0:
       x1,y1=lmList[8][1:]
       x2,y2=lmList[12][1:]
       print(x1,y1,x2,y2)
    # 3. Check which fingers are up detects which finger is up
       fingers=detector.fingersUp()
       # print(fingers)
    # 4. Only Index Finger : Moving Mode
       if fingers[1]==1 and fingers[2]==0:
  # 5. Convert Coordinates(we need to convert the coordinates  because  web cam gives 400*200 and our screen gives 1000*200)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        # instead of x3 and y3 we will send smothhen values
        x3=np.interp(x1,(frameR,wCam),(frameR,wScr))
        y3=np.interp(y1,(frameR,hCam),(frameR,hScr))

    # 6. Smoothen Values
        clocx=plocx+(x3-plocx)/smothening
        clocy = plocy + (x3 - plocy) / smothening
    # 7. Move Mouse
    # in this when we are moving to right it moves to left so we have to flip it
    #     autopy.mouse.move(x3,y3)
        autopy.mouse.move(wScr-x3, y3)
    #         drawing circle to our middle finger
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        plocx,plocy=clocx,clocy
    # 8. Both Index and middle fingers are up : Clicking Mode
       if fingers[1]==1 and fingers[2]==1:
        # it will find out the distance between the index and middle finger and if the distance is less than certain point we will make the mouse click
        length,img,lineInfo=detector.findDistance(8,12,img)
        print(length)
        if length<35:
            # cx and cy are last two values
            cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()
    # 9. Find distance between fingers
    # 10. Click mouse if distance short
    # 11. Frame Rate(how fast the object is moving)
    # finding current time
    cTime = time.time()
    # fps formula
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # as fps will be an integer so typcasting to str
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)

    # 12. Display
    cv2.imshow('image', img)
    cv2.waitKey(1)