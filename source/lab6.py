import cv2  # импорт модуля cv2
import numpy as np

# cv2.VideoCapture("видеофайл.mp4"); вывод кадров из видео файла
cap = cv2.VideoCapture(0);  # видео поток с веб камеры

cap.set(3, 1280)  # установка размера окна
cap.set(4, 700)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():  # метод isOpened() выводит статус видеопотока

    diff = cv2.absdiff(frame1,
                       frame2)  # нахождение разницы двух кадров, которая проявляется лишь при изменении одного из них, т.е. с этого момента наша программа реагирует на любое движение.

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # перевод кадров в черно-белую градацию

    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # фильтрация лишних контуров

    _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)  # метод для выделения кромки объекта белым цветом

    #dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(
            contour)  # преобразование массива из предыдущего этапа в кортеж из четырех координат


        if cv2.contourArea(contour) < 700:  # условие при котором площадь выделенного объекта меньше 700 px
            continue
        cv2.drawContours(frame1, contour, -1, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.putText(frame1, "Status: {}".format("Dvigenie"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                    cv2.LINE_AA)


    cv2.imshow("frame1", frame1)
    frame1 = frame2  #
    ret, frame2 = cap.read()  #

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
