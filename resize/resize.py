import cv2, glob

images=glob.glob("*.jpg")

for image in images:
    img = cv2.imread(image,0)

    re=cv2.resize(img, (int(img.shape[1]/25), int(img.shape[0]/18.75)), interpolation = cv2.INTER_AREA)

    cv2.imshow("cek",re)

    cv2.waitKey(500)
    cv2.destroyAllWindows()
	
    cv2.imwrite("resize/"+image, re)