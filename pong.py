import cv2
import time
from cvzone.HandTrackingModule import HandDetector
import numpy as np


# Variables for FPS
font = cv2.FONT_HERSHEY_SIMPLEX
prev_frame_time = 0
new_frame_time = 0
frame_number = 0
fps = "none"

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Game Elements Variables
color = (250, 250, 250)
ballPosX = 220
ballPosY = 45
speedX = 10
speedY = 10
y1 = 30
start_point = (620, 30)
end_point = (640, 110)

# Game Logic Variables
quit_game = False
score = 0

# Video capture device number and setting
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 864)
cap.set(4, 480)

# Reading images
img_background = cv2.imread("assets/background.png")

while True:

    # Read frame
    _, frame = cap.read()
    if not _:
        break

    # Detecting hands
    frame = cv2.flip(frame, 1)
    hands, img = detector.findHands(frame, flipType=False)

    # Overlay image
    frame = cv2.addWeighted(frame, 0.2, img_background, 0.8, 0)

    # Move Ball
    if ballPosY >= 360 or ballPosY <= 35:
        speedY = -speedY
    if ballPosX <= 210:
        speedX = -speedX
    ballPosX += speedX
    ballPosY += speedY

    # Draw Ball
    frame = cv2.circle(frame, (ballPosX, ballPosY), 10, (240, 240, 240), -1)

    # Check for hand and drawing paddle
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            y1 = np.clip(y, 30, 285)
            start_point = (620, 0+y1)
            end_point = (640, 80+y1)
    frame = cv2.rectangle(frame, start_point, end_point, color, -1)

    # Draw Walls
    frame = cv2.rectangle(frame, (200, 25), (664, 370), color, 10)

    # Shaw Score
    cv2.putText(frame, "Score:", (7, 70), font, 1, (255, 255, 255), 4, cv2.LINE_AA)
    cv2.putText(frame, str(score), (7, 140), font, 2, (255, 255, 255), 4, cv2.LINE_AA)

    # Show FPS on screen
    frame_number += 1
    new_frame_time = time.time()
    if frame_number % 5 == 0:
        fps = 1 / (new_frame_time - prev_frame_time)
        fps = int(fps)
        fps = str(fps)
    prev_frame_time = new_frame_time
    cv2.putText(frame, "Fps:", (700, 70), font, 1, (255, 255, 255), 4, cv2.LINE_AA)
    cv2.putText(frame, fps, (700, 140), font, 2, (255, 255, 255), 4, cv2.LINE_AA)

    # Check if ball hits paddle
    if ballPosX >= 615:
        if (y1 - 8) < ballPosY < (y1 + 80 + 8):
            speedX = -speedX
            score += 1
        else:
            break

    # Show frame
    cv2.imshow('Pong', frame)

    # Wait 1 msec
    if cv2.waitKey(1) & 0xFF == ord('q'):
        quit_game = True
        break

# If not Quit, place Game Over text
if not quit_game:
    cv2.putText(frame, "Game Over", (165, 200), font, 3, (100, 100, 100), 20, cv2.LINE_AA)
    cv2.putText(frame, "Game Over", (165, 200), font, 3, (255, 255, 255), 6, cv2.LINE_AA)
    cv2.imshow("Pong", frame)
    cv2.waitKey(0)

# Release the capture and destroy the all windows
cap.release()
cv2.destroyAllWindows()
