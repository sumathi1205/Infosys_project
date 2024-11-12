import cv2
import numpy
import matplotlib.pyplot as plt


img = cv2.imread(r"C:\Users\nithin\Documents\Infosys\Infosys\sample\Blood.jpg")

cv2.imshow("Original_Image",img)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray_Image",gray)

blur = cv2.GaussianBlur(gray,(5,5),0)
cv2.imshow('"Blurred_Image',blur)

val1,threshold = cv2.threshold(blur,120,255,cv2.THRESH_BINARY)
cv2.imshow("Threshold_Image",threshold)

contour, val2 = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(contour)

contour_len = len(contour)
print(contour_len)
if(contour_len<50):
    print('O')
elif(50 <= contour_len < 100):
    print("A")
elif(100 <= contour_len < 150):
    print("B")
else:
    print("AB")

cv2.waitKey(0)

cv2.destroyAllWindows()
