from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import pyautogui
import requests
import time

# читаем список user_id из файла
with open('id.txt', 'r') as file:
    user_ids = [line.strip() for line in file.readlines()]

# читаем пароль из файла
with open('password.txt', 'r') as file:
    metamask_password = file.read().strip()


# функция для закрытия браузера по user_id
def close_browser(user_id):
    try:
        close_url = f"http://local.adspower.net:50325/api/v1/browser/stop?user_id={user_id}"
        requests.get(close_url).json()
    except Exception as e:
        print(f"Error while closing browser for {user_id}: {str(e)}")


# основная функция
def main():
    # основной цикл по каждому user_id
    for user_id in user_ids:
        if user_id.lower() == 'stop':
            break

        driver = None
        start_time = datetime.now()

        try:
            # открываем браузер для текущего user_id
            open_url = f"http://local.adspower.net:50325/api/v1/browser/start?user_id={user_id}"
            response = requests.get(open_url).json()

            # настройка ChromeDriver для удалённого подключения
            chrome_driver = response["data"]["webdriver"]
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", response["data"]["ws"]["selenium"])

            service = Service(executable_path=chrome_driver)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_window_size(1200, 720)

            # открываем кошелек мм и вводим пароль
            driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock')
            time.sleep(2)
            password_field = driver.find_element(By.XPATH, '//*[@id="password"]')
            password_field.send_keys(metamask_password)
            time.sleep(1)
            continue_button = driver.find_element(By.XPATH, '//button[contains(text(), "Разблокировать")]')
            continue_button.click()
            time.sleep(3)

            # выполняем 1 миссию на сайте
            driver.get('https://mission.swanchain.io/')
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="tab-OnchainMission"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="el-collapse-head-8"]/div/div/div[3]').click()
            time.sleep(5)

            # открываем новое окно и подписываем транзакцию
            driver.switch_to.new_window('window')
            time.sleep(2)
            driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock')
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[3]/button[2]').click()
            time.sleep(5)

            # возвращаемся к mission.swanchain.io и начинаем выполнение 2 задания
            driver.get('https://mission.swanchain.io/')
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="tab-OnchainMission"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="el-collapse-head-9"]/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="el-collapse-content-9"]/div/div/span/span/span').click()
            time.sleep(2)

            # клик на кнопку "mint"
            x_click = 800
            y_click = 480
            pyautogui.click(x_click, y_click)
            time.sleep(5)

            # открываем ещё одно новое окно и подписываем транзакцию
            driver.switch_to.new_window('window')
            time.sleep(2)
            driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock')
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[3]/button[2]').click()
            time.sleep(5)

            # завершение миссии 2
            driver.get('https://mission.swanchain.io/')
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="tab-OnchainMission"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="el-collapse-head-9"]/div').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="el-collapse-head-9"]/div/div/div[3]').click()
            time.sleep(5)

            end_time = datetime.now()
            print(
                f"Completed work: {user_id} from {start_time.strftime('%Y-%m-%d %H:%M:%S')} to"
                f" {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Error while working with {user_id}: {str(e)}")
            with open('error.txt', 'a') as error_file:
                error_file.write(f"{user_id}: {str(e)}\n")

        finally:
            # закрытие браузера в любом случае
            close_browser(user_id)
            if 'driver' in locals():
                driver.quit()


# запуск основной функции
if __name__ == "__main__":
    main()
