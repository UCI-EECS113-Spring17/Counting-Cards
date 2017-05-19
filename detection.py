import numpy as np
import cv2

card_cascade = cv2.CascadeClassifier('mypokerdetector_3whole.xml')
img=cv2.imread('test.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cards = card_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
print "Found {0} cards!".format(len(cards))
for (x,y,w,h) in cards:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
