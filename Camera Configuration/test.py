
import numpy as np
import cv2
def nothing(x):
        pass

cap=cv2.VideoCapture(1)
##cap.set(cv2.CAP_PROP_HUE,1)
##cap.set(cv2.CAP_PROP_FPS,20)
##cap.set(cv2.CAP_PROP_BRIGHTNESS,10)
##bright=cap.get(cv2.CAP_PROP_BRIGHTNESS)
##sat=cap.set(cv2.CAP_PROP_SATURATION,50)
##cont=cap.set(cv2.CAP_PROP_CONTRAST,200)
##cap.set(cv2.CAP_PROP_EXPOSURE,15)
##
##iso=cap.get(cv2.CAP_PROP_ISO_SPEED)
cap.set(cv2.CAP_PROP_CONTRAST,32)
print cap.get(cv2.CAP_PROP_CONTRAST)#32
cap.set(cv2.CAP_PROP_EXPOSURE,-4)#-3
print cap.get(cv2.CAP_PROP_EXPOSURE)#-6





##print expo




cv2.namedWindow('Colorbars') #Create a window named 'Colorbars'
 
#assign strings for ease of coding
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'
wnd = 'Colorbars'
#Begin Creating trackbars for each
cv2.createTrackbar(hl, wnd,0,179,nothing)
cv2.createTrackbar(hh, wnd,0,179,nothing)
cv2.createTrackbar(sl, wnd,0,255,nothing)
cv2.createTrackbar(sh, wnd,0,255,nothing)
cv2.createTrackbar(vl, wnd,0,255,nothing)
cv2.createTrackbar(vh, wnd,0,255,nothing)


        
while True:
        ret, frame = cap.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),3 )
        ret,white= cv2.threshold(blur,15,255,0)
        edges = cv2.Canny(gray,140,160)
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #read trackbar positions for each trackbar
        hul=cv2.getTrackbarPos(hl, wnd)
        huh=cv2.getTrackbarPos(hh, wnd)
        sal=cv2.getTrackbarPos(sl, wnd)
        sah=cv2.getTrackbarPos(sh, wnd)
        val=cv2.getTrackbarPos(vl, wnd)
        vah=cv2.getTrackbarPos(vh, wnd)
 
        #make array for final values
        HSVLOW=np.array([hul,sal,val])
        HSVHIGH=np.array([huh,sah,vah])
        
        GREENL=np.array([50,0,70])
        GREENH=np.array([100,255,255])

        REDL=np.array([5,51,118])
        REDH=np.array([37,251,255])

        BLUEL=np.array([50,0,0])
        BLUEH=np.array([130,200,70])

        BLACKL=np.array([0,57,0])
        BLACKH=np.array([63,232,90])

        WHITEL=np.array([0,0,0])
        WHITEH=np.array([0,255,255])
 
        #create a mask for that range
        mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
        #mask = cv2.erode(mask, None, iterations=2)
        #mask = cv2.dilate(mask, None, iterations=2)
        greenmask = cv2.inRange(hsv,GREENL, GREENH)
        redmask = cv2.inRange(hsv,REDL, REDH)
        bluemask = cv2.inRange(hsv,BLUEL, BLUEH)
        blackmask = cv2.inRange(hsv,BLACKL, BLACKH)
        whitemask = cv2.inRange(hsv,WHITEL, WHITEH)





        
        
        res = cv2.bitwise_and(frame,frame, mask =mask)
     

        
 
        cv2.imshow(wnd, res)

        #find cards
        im2,contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for i in contours:
                if 500<cv2.contourArea(i)<100000:

                        peri = cv2.arcLength(i,True)
                        approx = cv2.approxPolyDP(i,0.01*peri,True)
                        approx=np.float32(approx)
                        
                        #rect = cv2.minAreaRect(i)
                        #box = cv2.boxPoints(rect)
                        #box = np.int0(box)
                        #cv2.drawContours(frame,[box],0,(0,0,255),1)

                        if len(approx)==4:
                                cv2.drawContours(frame,[i],0,(0,255,0),3)

                                h = np.array([[0,0],[0,250],[200,250],[200,0]],np.float32)
                                transform = cv2.getPerspectiveTransform(approx,h)
                                warp = cv2.warpPerspective(frame,transform,(200,250))
                                cv2.imshow('card',warp)

   
                        
        #find chips
        im2,contours2, hierarchy = cv2.findContours(white,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        redcount=0
        greencount=0
        bluecount=0
        blackcount=0
        whitecount=0

        redl=117
        redh=148

        greenl=105
        greenh=116

        whitel=94
        whiteh=106

        bluel=78
        blueh=83

        blackl=73
        blackh=77     


        
        for i in contours2:
                        if 500<cv2.contourArea(i)<10000:#3000

                                peri = cv2.arcLength(i,True)
                                approx = cv2.approxPolyDP(i,0.01*peri,True)
                                approx=np.float32(approx)
                                
                                if len(approx)>4:
                                        x,y,w,h = cv2.boundingRect(i)
                                        offsetx=w/3
                                        offsety=h/3
                                        rect=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                                        roi=frame[y+offsety:y+h-offsety,x+offsetx:x+w-offsetx]
                                        cv2.imshow("chip",roi)
                                        hsv2=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                                        mean=hsv2.mean()
                                        h=hsv2[0][0][0]
                                        s=hsv2[0][0][1]
                                        v=hsv2[0][0][2]
                                        print hsv2[0][0]

                                        
                                        if  h>150 or h <10:
                                                redcount+=1
                                        elif v<50:
                                                blackcount+=1
                                        elif h>100 and s>100 and v>50:
                                                bluecount+=1
                                        elif  v>110:
                                                whitecount+=1      
                                        elif h<110:
                                                greencount+=1

                                        

                                                
        if redcount!=0:
                cv2.putText(frame, "Red Object Detected"+str(redcount), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)

        if greencount!=0:
                cv2.putText(frame, "Green Object Detected"+str(greencount), (10,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)

        if whitecount!=0:
                cv2.putText(frame, "White Object Detected"+str(whitecount), (10,140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)

        if bluecount!=0:
                cv2.putText(frame, "Blue Object Detected"+str(bluecount), (10,160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)

        if blackcount!=0:
                cv2.putText(frame, "Black Object Detected"+str(blackcount), (10,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)

##                                        greenres = cv2.bitwise_and(frame[x:x+w,y+y+h],frame[x:x+w,y+y+h], mask =greenmask)
##                                        redres = cv2.bitwise_and(frame,frame, mask =redmask)
##                                        blueres = cv2.bitwise_and(frame,frame, mask =bluemask)
##                                        blackres = cv2.bitwise_and(frame,frame, mask =blackmask)
##                                        whiteres = cv2.bitwise_and(frame,frame, mask =whitemask)


##        ret,threshold = cv2.threshold(cv2.cvtColor(res,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
##        ret,greenthresh = cv2.threshold(cv2.cvtColor(greenres,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
##        ret,redthresh = cv2.threshold(cv2.cvtColor(redres,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
##        ret,bluethresh = cv2.threshold(cv2.cvtColor(blueres,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
##        ret,blackthresh = cv2.threshold(cv2.cvtColor(blackres,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
##        ret,whitethresh = cv2.threshold(cv2.cvtColor(whiteres,cv2.COLOR_BGR2GRAY),3,255,cv2.THRESH_BINARY)
##
##
####        im2,contours2, hierarchy = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##        im2,greencontours2, hierarchy = cv2.findContours(greenthresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##        im2,redcontours2, hierarchy = cv2.findContours(redthresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##        im2,bluecontours2, hierarchy = cv2.findContours(bluethresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##        im2,blackcontours2, hierarchy = cv2.findContours(blackthresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##        im2,whitecontours2, hierarchy = cv2.findContours(whitethresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
##
##
##
##        count=0
##        for i in greencontours2:
##
##                        if 1000<cv2.contourArea(i)<100000:
##                                peri3 = cv2.arcLength(i,True)
##                                approx3 = cv2.approxPolyDP(i,0.01*peri3,True)
##                                approx3=np.float32(approx3)
##
##         
##                                
##                                if len(approx3)>8:
##                                        count+=1
##                                        cv2.drawContours(frame,[i],0,(255,0,0),3)
##
##        if count!=0:
##                cv2.putText(frame, "Green Object Detected"+str(count), (10,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)
##
##
##        count=0
##        for i in redcontours2:
##                
##
##                        if 1000<cv2.contourArea(i)<100000:
##                                peri4 = cv2.arcLength(i,True)
##                                approx4 = cv2.approxPolyDP(i,0.01*peri4,True)
##                                approx4=np.float32(approx4)
##
##         
##                                
##                                if len(approx4)>8:
##                                        count+=1
##                                        cv2.drawContours(frame,[i],0,(255,0,0),3)
##        if count!=0:
##                cv2.putText(frame, "Red Object Detected"+str(count), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)
##
##        count=0
##        for i in bluecontours2:
##
##                        if 500<cv2.contourArea(i)<100000:
##                                peri4 = cv2.arcLength(i,True)
##                                approx4 = cv2.approxPolyDP(i,0.01*peri4,True)
##                                approx4=np.float32(approx4)
##
##         
##                                
##                                if len(approx4)>8:
##                                        count+=1
##                                        cv2.drawContours(frame,[i],0,(255,0,0),3)
##
##        if count!=0:
##                cv2.putText(frame, "Blue Object Detected"+str(count), (10,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)
##
####        for i in blackcontours2:
####
####                        if 1000<cv2.contourArea(i)<100000:
####                                peri4 = cv2.arcLength(i,True)
####                                approx4 = cv2.approxPolyDP(i,0.01*peri4,True)
####                                approx4=np.float32(approx4)
####
####         
####                                
####                                if len(approx4)>8:
####                                        cv2.drawContours(frame,[i],0,(255,0,0),3)
####                                        cv2.putText(frame, "Black Object Detected", (10,140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)
##
##        count=0
##        for i in whitecontours2:
##
##                        if 250<cv2.contourArea(i)<2000:
##                                peri4 = cv2.arcLength(i,True)
##                                approx4 = cv2.approxPolyDP(i,0.01*peri4,True)
##                                approx4=np.float32(approx4)
##
##         
##                                
##                                if len(approx4)>8:
##                                        count+=1
##                                        cv2.drawContours(frame,[i],0,(255,0,0),3)
##        if count!=0:
##                cv2.putText(frame, "White Object Detected"+str(count), (10,160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),1)


        
                        
        cv2.imshow('frame',frame)
##        cv2.imshow('blur',blur)

        cv2.imshow('white',white)
        cv2.imshow('edges',edges)
##        cv2.imshow('mask',threshold)


      

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

cap.release()
cv2.destroyAllWindows()
