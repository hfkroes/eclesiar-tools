import pyautogui
import pyperclip
import time

transactions = ""
page_number = 1
pages_to_be_read = 22
holding = 1

coord_dict_start = {1: 750, 2: 790, 3: 830, 4: 870, 5: 910}
coord_dict_end = {1: 1040, 2: 1000, 3: 960}

def determine_total_pages():
    pyautogui.click()
    pyautogui.moveTo(1060, 890)
    time.sleep(0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(1025, 890)
    pyautogui.mouseUp()
    pyautogui.hotkey('ctrl', 'c')
    total_pages = int(pyperclip.paste())
    return total_pages

def click_next_page(page_number):
    to_end = total_pages - page_number
    if page_number < 6:
        x = coord_dict_start[page_number]
        pyautogui.moveTo(x, 890)
    elif to_end == 0:
        pass
    elif to_end < 4:
        x = coord_dict_end[to_end]
        pyautogui.moveTo(x, 890)
    else:
        pyautogui.moveTo(920, 890)
    pyautogui.click()

def copy_page(transactions):
    if holding == 1:
        pyautogui.moveTo(700, 390)
    else:
        pyautogui.moveTo(700, 430)
    pyautogui.click()
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'end')
    time.sleep(0.1)
    pyautogui.moveTo(1525, 815)
    pyautogui.mouseUp()
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    transactions = transactions + pyperclip.paste()
    return transactions

for i in range(1, pages_to_be_read + 1):
    print(page_number)
    transactions = copy_page(transactions)
    if page_number == 1:
        total_pages = determine_total_pages()
    click_next_page(page_number)
    time.sleep(1.0)
    page_number += 1

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(transactions)