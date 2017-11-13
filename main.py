import numpy as np
import cv2
import platform
from HarrisCorner import findCorners
from Draw import markWithCircle
from LucasKanade import trackFeatures


# Video Reader
cap = cv2.VideoCapture("Videos/mouse.mp4")

# Video Writer
fourcc = cv2.VideoWriter_fourcc(*'IYUV')

out = cv2.VideoWriter(
    'result.avi',
    fourcc,
    cap.get(cv2.CAP_PROP_FPS),
    (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
     int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
)

ret, old_frame = cap.read()
old_frame_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

corner_num = 1
frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
row_list = np.zeros((corner_num, frame_num + 1))
col_list = np.zeros((corner_num, frame_num + 1))
# Find corners on the first frame
r, c = findCorners(old_frame_gray, 11, corner_num)
row_list[:, int(cap.get(cv2.CAP_PROP_POS_FRAMES))] = r
col_list[:, int(cap.get(cv2.CAP_PROP_POS_FRAMES))] = c


while(1):
    ret, new_frame = cap.read()

    if(not ret):
        print "no frame to read"
        break

    new_frame_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)

    r, c = trackFeatures(old_frame_gray, new_frame_gray, r, c)
    row_list[:, int(cap.get(cv2.CAP_PROP_POS_FRAMES))] = r
    col_list[:, int(cap.get(cv2.CAP_PROP_POS_FRAMES))] = c
    #cv2.imshow('frame', markWithCircle(r, c, new_frame))

    out.write(markWithCircle(r, c, new_frame))

    # break when ESC is pressed
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break

    old_frame = new_frame
    old_frame_gray = new_frame_gray

np.savetxt("rows.csv", row_list, delimiter=",")
np.savetxt("cols.csv", row_list, delimiter=",")

cv2.destroyAllWindows()
out.release()
cap.release()
