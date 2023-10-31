import numpy as np
import pyautogui
import cv2
from imutils.object_detection import non_max_suppression
from time import sleep

# find templates
# for x in range(8):
#     for y in range(7):
#         if x > 3 and y == 6: continue
#         sleep(0.2)
#         img = pyautogui.screenshot('current_shot.png', region=(90 + x*148, 219 + y*45, 120, 35))
#         img = cv2.imread('current_shot.png')
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         cv2.imwrite(f'plates/{x + 1}_{y + 1}.png',img)

def fetch_board_state():
    pyautogui.hotkey('alt', 'tab')
    sleep(0.1)
    pyautogui.screenshot('current_game.jpg')
    screenshot = cv2.imread('current_game.jpg')
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    threshold = 0.95
    all_coords = {}
    for value in range(1, 14):
        for suit in range(4):
            template = cv2.imread(f'templates/{value}-{suit}.png', 0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            coords = [(x, y, x + w, y + h) for x, y in zip(*loc[::-1])]
            coords = non_max_suppression(np.array(coords)) 
            for (x, y, xx, yy) in coords:
                cv2.rectangle(screenshot, (x, y), (xx, yy), (255, 0, 0), 2)
                # pyautogui.doubleClick(x + w/2, y + h/2)
                sleep(0.1)
            simple_coord = list(coords[0])
            all_coords[(value, suit)] = [round(simple_coord[0], -1), round(simple_coord[1], -1)]
    pyautogui.hotkey('alt', 'tab')
    cv2.imwrite('result.png',screenshot)

    for card, coords in all_coords.items():
        print(card, coords)
    return all_coords

def main():
    fetch_board_state()

if __name__ == '__main__':
    main()


