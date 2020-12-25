import time
from datetime import datetime
import sched
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import eel
import os
import tkinter.filedialog
import atexit
import sys

driver_path = './chromedriver.exe'

meet_url = 'https://meet.google.com/'
meet_room = None
login_url = 'https://www.google.com/accounts?hl=ja-JP'

login_id = None
login_pw = None

login_time = None
logout_time = None

open_window = False
mute_window = True

scheduler = sched.scheduler(time.time, time.sleep)
login_sd = None
logout_sd = None
check_sd = None
is_login = False
driver = None

use_date = True
use_Number = False
max_room_number = 0
logout_rate = 50
type_or = True


@eel.expose
def reset_system():
    global scheduler, login_sd, logout_sd, check_sd, is_login, driver
    if login_sd is not None and not scheduler.empty():
        scheduler.cancel(login_sd)
        login_sd = None
    if logout_sd is not None and not scheduler.empty():
        scheduler.cancel(logout_sd)
        logout_sd = None
    if check_sd is not None and not scheduler.empty():
        scheduler.cancel(check_sd)
        check_sd = None
    if is_login and driver is not None:
        logout_meet()
        is_login = False
    elif driver is not None:
        driver.close()
        driver.quit()
        driver = None
        eel.show_log('Success Cancel')
        eel.on_complete()


@eel.expose
def load_data(file_name):
    if file_name == "":
        fTyp = [("", "*.txt")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        root = tkinter.Tk()
        root.withdraw()
        file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        root.destroy()
        if len(file_name) == 0:
            eel.show_log("File not selected.")
            return
    elif len(file_name) == 0:
        return
    with open(file_name) as f:
        return f.read()


@eel.expose
def save_data(args):
    iDir = os.path.abspath(os.path.dirname(__file__))
    root = tkinter.Tk()
    root.withdraw()
    folder_name = tkinter.filedialog.askdirectory(initialdir=iDir)
    root.destroy()
    if len(folder_name) == 0:
        eel.show_log("Folder not selected.")
        return
    with open(folder_name + "/identifier.txt", mode='w') as f:
        f.write(",".join(args))
    eel.show_log("Save Identifier at '" + folder_name + "/identifier.txt'")
    return


@eel.expose
def set_value(args):
    global login_id, login_pw, meet_room, login_time, logout_time, open_window, mute_window, use_date, use_Number, logout_rate, type_or
    login_id = args[0]
    login_pw = args[1]
    if login_id == "" or login_pw == "":
        eel.show_log_error('Load Failed: Unexpected Google Account')
        return False

    #removed_url = args[2].removeprefix(meet_url)
    removed_url = args[2][len(meet_url):] if args[2].startswith(meet_url) else args[2]
    if len(removed_url.split('-')) != 3:
        eel.show_log_error('Load Failed: Unexpected Meet URL')
        return False
    meet_room = removed_url

    year, month, day = map(int, args[3].split('-'))
    hour, min = map(int, args[4].split(':'))
    login_time = datetime(year, month, day, hour, min, 0)
    year, month, day = map(int, args[5].split('-'))
    hour, min = map(int, args[6].split(':'))
    logout_time = datetime(year, month, day, hour, min, 0)

    open_window = args[7]
    mute_window = args[8]

    use_date = args[9]
    use_Number = args[10]
    logout_rate = int(args[11])
    type_or = args[12]
    eel.show_log('Load Success')
    return args


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def setup():
    global open_window
    opt = Options()
    opt.add_argument('--disable-gpu')
    if not open_window:
        opt.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36')
        opt.add_argument('--headless')
        opt.add_argument("--window-size=1920,1080")
    opt.add_argument("use-fake-device-for-media-stream")
    opt.add_argument("use-fake-ui-for-media-stream")
    if mute_window:
        opt.add_argument("--mute-audio")
    opt.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    })
    eel.show_log('Driver Open')
    return webdriver.Chrome(executable_path=resource_path(driver_path), options=opt)


def login_google():
    global login_time, driver
    if driver is None:
        return
    driver.get(login_url)
    TIME_OUT = 5
    eel.show_log('Apply Google ID')
    WebDriverWait(driver, TIME_OUT).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
    ).send_keys(login_id + Keys.ENTER)

    eel.show_log('Apply Google Password')
    while True:
        try:
            WebDriverWait(driver, TIME_OUT).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
            ).send_keys(login_pw + Keys.ENTER)
            break
        except Exception:
            continue
    eel.sleep(5)
    eel.show_log('Success Google Login<br>Wait Login at ' + login_time.strftime('%Y/%m/%d %H:%M'))


def login_meet():
    global is_login, driver, meet_url, meet_room, use_Number, use_date, logout_rate, type_or
    if driver is None:
        return
    TIME_OUT = 5
    eel.show_log(f'Access Meet Room: ID "{meet_room}"<br>Now preparing to enter the room...(1/4)')
    driver.get(meet_url + meet_room)
    eel.sleep(1)
    eel.show_log(f'Access Meet Room: ID "{meet_room}"<br>Now preparing to enter the room...(2/4)')
    driver.get(meet_url + meet_room)
    eel.sleep(1)
    eel.show_log(f'Access Meet Room: ID "{meet_room}"<br>Now preparing to enter the room...(3/4)')
    driver.get(meet_url + meet_room)
    eel.sleep(1)
    eel.show_log(f'Access Meet Room: ID "{meet_room}"<br>Now preparing to enter the room...(4/4)')
    WebDriverWait(driver, TIME_OUT).until(
        EC.presence_of_element_located((By.XPATH, '/html/body'))
    ).send_keys(Keys.CONTROL, "de")
    eel.sleep(1)
    try:
        is_login = True
        WebDriverWait(driver, TIME_OUT).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span'))
        ).click()
    except exceptions.ElementNotInteractableException as eex:
        print(eex)
        element = driver.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span')
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(element, 5, 5)
        action.click()
        action.perform()
    except Exception as ex:
        eel.show_log_error("Failed to login")
        reset_system()
        print(ex.with_traceback)
        for entry in driver.get_log('browser'):
            print(entry)
        return
    message = 'Login Success'
    if use_date:
        message = message + '<br>Wait Logout at ' + logout_time.strftime('%Y/%m/%d %H:%M')
    if use_date and use_Number:
        message = message + (' or ' if type_or else ' and ')
    if use_Number:
        message = message + 'Wait Participant number Less than ' + str(logout_rate) + '% of the maximum number'
    eel.show_log(message)


def logout_meet():
    global is_login, driver, type_or
    if driver is None:
        return
    driver.refresh()
    is_login = False
    driver.close()
    driver.quit()
    driver = None
    eel.show_log('Success Logout')
    eel.on_complete()


def run_at_target_time(target: datetime, func):
    global scheduler
    delay = (target - datetime.now()).total_seconds()
    if delay > 0:
        return scheduler.enter(delay, 1, func)
    else:
        func()
        return None


def check_room_number():
    global max_room_number, type_or, scheduler, check_sd, driver
    current_room_number = int(driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[8]/div[3]/div[6]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]').get_attribute('innerHTML'))
    if current_room_number > max_room_number:
        max_room_number = current_room_number
    elif max_room_number * logout_rate / 100 >= current_room_number:
        if type_or:
            logout_meet()
            return
        else:
            type_or = True
    check_sd = scheduler.enter(1, 1, check_room_number)
    scheduler.run()


def complete_date():
    global type_or
    if type_or:
        logout_meet()
    else:
        type_or = True


@eel.expose
def start_system():
    global login_sd, logout_sd, check_sd, driver, login_time, logout_time, scheduler
    driver = setup()
    login_google()
    login_sd = run_at_target_time(login_time, login_meet)
    if use_date:
        logout_sd = run_at_target_time(logout_time, complete_date)
    if use_Number:
        check_sd = scheduler.enter(1, 1, check_room_number)
    threading.Thread(target=scheduler.run).start()


atexit.register(reset_system)
eel.init('web')
eel.start('main.html', size=(560, 680), port=0)
