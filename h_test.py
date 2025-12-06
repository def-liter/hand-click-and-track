import cv2
import mediapipe as mp
import pyautogui
import keyboard
import time

pause = False
cap_hand = mp.solutions.hands.Hands()
drawing_options = mp.solutions.drawing_utils
camera = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

last_click_time = 0
click_cooldown = 0.5 

while True:
    ret, image = camera.read()
    if not ret or image is None:
        continue
    image_height, image_width, res = image.shape
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = cap_hand.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    if keyboard.is_pressed('`'):
        pause = not pause
        time.sleep(0.2)
        print("paused")
    if pause != True:
        if all_hands:
            for hand in all_hands:
                drawing_options.draw_landmarks(image, hand)
                one_hand_landmarks = hand.landmark
                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)
                    if id == 8:
                        mouse_x = screen_width / image_width * x
                        mouse_y = screen_height / image_height * y
                        cv2.circle(image, (x, y), 10, (255,0,255))
                        x1 = x
                        y1 = y
                        pyautogui.moveTo(mouse_x, mouse_y)
                    if id == 4:
                        cv2.circle(image, (x, y), 10, (255,0,255))
                        x2 = x
                        y2 = y
            dist = abs(y2 - y1)
            print(dist)
            if dist < 17 and (time.time() - last_click_time) > click_cooldown:
                pyautogui.click(clicks=1)
    else:
        pass
            
    cv2.imshow("hand_m", image)
    key = cv2.waitKey(1)
    if keyboard.is_pressed('q'):
        break
        
    
camera.release()
cv2.destroyAllWindows()