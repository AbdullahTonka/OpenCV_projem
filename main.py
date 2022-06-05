import time
import cv2
import keyboard
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

r = 0
IMAGE_FILES = []
with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.flip(cv2.imread(file), 1)
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        print('Handedness:', results.multi_handedness)
        if not results.multi_hand_landmarks:
            continue
        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            print('hand_landmarks:', hand_landmarks)
            print(
                f'Index finger tip coordinates: (',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
            )
            mp_drawing.draw_landmarks(
                annotated_image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        cv2.imwrite(
            '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                ## el açık ve kapalı iken ekrana yazdırma
                x = hand_landmarks.landmark[5].x
                y = hand_landmarks.landmark[5].y
                x1 = hand_landmarks.landmark[4].x
                y1 = hand_landmarks.landmark[8].y

                font = cv2.FONT_HERSHEY_PLAIN

                if x1 < x and y1 < y :#FREN
                    keyboard.press('space')
                    keyboard.release('w')
                    keyboard.release('a')
                    keyboard.release('d')
                    cv2.putText(image, "Fren", (10, 50), font, 4, (0, 0, 255), 4)

                elif x1 > x and y1 > y:#İLERİ
                    keyboard.press('w')
                    keyboard.release('space')
                    keyboard.release('a')
                    keyboard.release('d')
                    cv2.putText(image, "Ileri", (10, 50), font, 4, (0, 0, 255), 4)

                elif x1 < x and y1 > y:#SOL
                    keyboard.press('a')
                    keyboard.press('w')
                    keyboard.release('d')
                    keyboard.release('space')
                    cv2.putText(image, "Sol", (10, 50), font, 4, (0, 0, 255), 4)

                elif x1 > x and y1 < y:#SAĞ
                    keyboard.press('d')
                    keyboard.press('w')
                    keyboard.release('a')
                    keyboard.release('space')
                    cv2.putText(image, "Sag", (10, 50), font, 4, (0, 0, 255), 4)
                else:
                    keyboard.release('space')
                    keyboard.release('a')
                    keyboard.release('d')
                    keyboard.release('w')
                if (x1 < x and y1 > y) or (x1 > x and y1 < y):
                    time.sleep(0.01)
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
cap.release()