# Import external packages.
from selenium.webdriver.common.by import By
import os
import errno
from winreg import *
import time


def get_user_downloads_folder():
    key = OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    a_path = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    return a_path


def delete_file(file_path_str):
    try:
        os.remove(file_path_str)
    except OSError as e:
        if e.errno != errno.ENOENT:     # 'errno.ENOENT' = no such file or directory.
            raise       # re-raise exception if a different error occurred.
    return


def enter_credentials(browser_window, a_time, user, psw2):
    # Entering credentials in the web page.
    # Enter user.
    user_elem = browser_window.find_element(
        By.XPATH,
        '/html/body/div[1]/div[2]/div[1]/div[3]/div[2]/div[1]/form/input[4]',
    )
    user_elem.send_keys(user)
    # Enter password.
    user_id_elem = browser_window.find_element(
        By.XPATH,
        '/html/body/div[1]/div[2]/div[1]/div[3]/div[2]/div[1]/form/input[5]',
    )
    user_id_elem.send_keys(psw2)
    # Click submit button.
    submit_elem = browser_window.find_element(
        By.XPATH,
        '/html/body/div[1]/div[2]/div[1]/div[3]/div[2]/div[1]/form/input[6]',
    )
    submit_elem.click()
    # wait sometime to build the page
    time.sleep(a_time)
    return


def calculate_average(x_list: list, y_list: list) -> float:
    """Returns a float average of the x_list and y_list values.
    x_list: list of values representing the % done.
    y_list: list of values representing the number of occurrences of a value x."""
    return round(sum([item[0] * item[1] for item in zip(y_list, x_list)]) / sum(y_list), 1)



