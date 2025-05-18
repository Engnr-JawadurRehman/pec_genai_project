import cv2

def capture_image(path='assets/captured.jpg'):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(path, frame)
    cap.release()
    return path
