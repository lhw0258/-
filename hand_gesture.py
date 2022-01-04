import time
import cv2
import numpy as np
import math
import pyautogui as pg


class Hand_Gesture:
    def __init__(self, mode, start):
        self.mode = mode
        self.start = start

    def change(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def run_app(self):
        cap = cv2.VideoCapture(0)
        while self.start:
            try:  # 如果它在窗口中找不到任何东西，就会出现错误，因为它找不到最大区域的轮廓
                # 因此，用一个捕捉异常语句
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                # 选取窗口
                roi = frame[0:300, 0:300]
                cv2.rectangle(frame, (0, 0), (300, 300), (0, 255, 0), 0)
                # 用HSV通道提取肤色特征
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                # 低阈值
                lower_skin = np.array([0, 20, 70], dtype=np.uint8)
                # 高阈值
                upper_skin = np.array([20, 255, 255], dtype=np.uint8)
                mask = cv2.inRange(hsv, lower_skin, upper_skin)
                # 高斯去噪5*5掩膜
                mask = cv2.GaussianBlur(mask, (5, 5), 100)
                # 5*5核
                kernel = np.ones(5 * 5, dtype=np.uint8)
                # 闭运算
                dst = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                # 寻找轮廓
                contours, _ = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                # 找到面积最大的轮廓
                cnt = max(contours, key=lambda x: cv2.contourArea(x))
                # 轮廓近似
                epsilon = 0.0005 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                # 获得凸形外壳
                hull = cv2.convexHull(cnt)
                # 获得凸形外壳面积
                area_hull = cv2.contourArea(hull)
                # 获得面积最大的轮廓
                area_cnt = cv2.contourArea(cnt)
                # 计算面积比
                area_ratio = ((area_hull - area_cnt) / area_cnt) * 100
                # 获得轮廓近似后的面积
                hull = cv2.convexHull(approx, returnPoints=False)
                # 找到凸型外壳缺失部位
                defects = cv2.convexityDefects(approx, hull)
                res = cv2.drawContours(dst, contours, -1, (255, 0, 255), 2)  # 绘制轮廓
                line = 0
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    se = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])

                    # 求三角形各边的长度
                    a = math.sqrt((end[0] - se[0]) ** 2 + (end[1] - se[1]) ** 2)
                    b = math.sqrt((far[0] - se[0]) ** 2 + (far[1] - se[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    s = (a + b + c) / 2
                    ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                    d = (2 * ar) / a
                    # 余弦定理求角度
                    angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                    if angle <= 90 and d > 30:
                        line += 1

                        cv2.circle(roi, far, 3, [255, 0, 0], -1)
                        # 在手上画线
                    cv2.line(roi, se, end, [0, 255, 0], 2)

                line += 1
                # 打印在其范围内的相应手势
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, str(self.mode), (0, 400), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                if line == 1:
                    if area_cnt < 2000:
                        cv2.putText(frame, 'Put hand in the box', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                    else:
                        if area_ratio < 12 and not self.mode:
                            cv2.putText(frame, '0', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                        elif area_ratio < 12 and self.mode:
                            pg.press('left')
                            time.sleep(1)
                        elif self.mode:
                            pg.press('right')
                            time.sleep(1)
                        else:
                            cv2.putText(frame, '1', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                elif line == 2 and not self.mode:
                    cv2.putText(frame, '2', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                elif line == 3 and not self.mode:
                    cv2.putText(frame, '3', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                elif line == 4 and not self.mode:
                    cv2.putText(frame, '4', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                elif line == 5 and not self.mode:
                    cv2.putText(frame, '5', (0, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.imshow("mask", res)
                cv2.imshow("frame", frame)
            except:
                pass
            key = cv2.waitKey(1)
            if key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

