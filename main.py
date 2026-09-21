import cv2
from datetime import datetime
import os

# Папкаларды түзүү
os.makedirs('Videos', exist_ok=True)
os.makedirs('Screenshots', exist_ok=True)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Камера жок')
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_fps = float(cap.get(cv2.CAP_PROP_FPS))

if frame_fps == 0:
    frame_fps = 30.0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

is_recording = False
out = None

print("Башкаруу баскычтары:")
print(" [S] - Скриншот алуу")
print(" [R] - Видео жазууну баштоо / токтотуу")
print(" [Q] - Программадан чыгуу")

while True:
    ret, frame = cap.read()
    if not ret:
        print('Кадр жок')
        break

    if is_recording and out is not None:
        out.write(frame)

        cv2.circle(frame, (30, 30), 8, (0, 0, 255), -1)
        cv2.putText(frame, 'REC', (45, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Camera', frame)

    key = cv2.waitKey(1) & 0xFF


    if key == ord('s'):
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        img_name = f'Screenshots/screenshot_{timestamp}.png'
        cv2.imwrite(img_name, frame)
        print(f'Скриншот сакталды: {img_name}')


    elif key == ord('r'):
        is_recording = not is_recording
        if is_recording:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            video_name = f'Videos/video_{timestamp}.mp4'
            out = cv2.VideoWriter(video_name, fourcc, frame_fps, (frame_width, frame_height))
            print(f'Видео жазуу башталды: {video_name}')
        else:
            if out is not None:
                out.release()
                out = None
            print('Видео жазуу токтотулду жана сакталды.')


    elif key == ord('q'):
        break

# Ресурстарды бошотуу
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()