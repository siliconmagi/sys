import pyscreenshot as ImageGrab
import cv2

img = ImageGrab.grab()
img.save("gray.png")
img2 = cv2.imread('gray.png')
gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray.png', gray)
