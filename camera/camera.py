import cv2

def capture(file_path):
	cap = cv2.VideoCapture(0)
	cap.set(10, 200)

	ret, frame = cap.read()

	out = cv2.imwrite(file_path, frame)

	cap.release()
	cv2.destroyAllWindows()
