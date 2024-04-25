import threading
import cv2
from deepface import DeepFace


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# set width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

face_match = False
counter = 0

andrew_img = cv2.imread("andrew_img.png")
mom_img = cv2.imread("mom_img.png")

people_counter = 0
people = ['Andrew', 'Mom']

def checkFace(frame, img, person):
    global face_match
    global people_counter
    if person == "Andrew":
        try:
            if DeepFace.verify(frame, andrew_img.copy())['verified']: # if face match true (current_frame, face_img)
                face_match = True
        except ValueError: # if face not detected
            face_match = False
    if person == "Mom":
        try:
            if DeepFace.verify(frame, mom_img.copy())['verified']: # if face match true (current_frame, face_img)
                face_match = True
        except ValueError: # if face not detected
            face_match = False

while True:
    ret, frame = cap.read()

    # make sure camera works
    if ret:
        # every 30 iterations
        if counter % 30 == 0: # if counter is a multiple of 30
            try:
                for i in range(2):
                    person = people[i]
                    if person == "Andrew":
                        image = "andrew_img.png"
                    if person == "Mom":
                        image = "mom_img.png"
                    threading.Thread(target=checkFace, args=(frame.copy(), image, person)).start()
                    if face_match and i == 1: # if face recognized after first attempt it doesn't have to do it again
                        people_counter = 1
                        break
                    if face_match and i == 2:
                        people_counter == 2
            except ValueError: # if face isn't recognized
                pass

        counter += 1

        print(people_counter)
        if face_match and people_counter == 1:
            cv2.putText(frame, f"ANDREW DETECTED", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3) # BGR Color
        if face_match and people_counter == 2:
            cv2.putText(frame, f"MOM DETECTED", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3) # BGR Color
        # if face_match:
        #     cv2.putText(frame, f"DETECTED", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3) # BGR Color
        if not face_match:
            cv2.putText(frame, "NO ONE DETECTED", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3) # BGR Color
        # else:
        #     print("Else")
        print(people_counter)

        cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()