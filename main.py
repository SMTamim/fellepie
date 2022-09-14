from selenium import webdriver
import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
import time, threading, sys, os

URL = 'https://a.aliexpress.com/_mqWnU8M'


def raiseException(err):
    print(err)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, file_name, exc_tb.tb_lineno)


def getDriver(headless=False):
    options = webdriver.ChromeOptions()
    # user_agents = [agent.replace('\n', '') for agent in open('user-agents.txt', 'r', encoding='utf-8').readlines()]
    # user_agent = random.choice(user_agents)
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    options.add_argument(f'--user-agent={user_agent}')
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


def firefoxDriver(headless=False):
    options = webdriver.FirefoxOptions()
    options.set_preference('s')
    # options.add_argument('--headless')
    return webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)


def main(email, password):
    driver = getDriver()
    # driver = firefoxDriver()
    actions = ActionChains(driver)
    driver.set_window_size(450, 900)
    driver.get(URL)
    wait = WebDriverWait(driver, 60)
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'div.rcButton--btn--EMLV5lz')))
    driver.find_element(By.CSS_SELECTOR, 'div.rcButton--btn--EMLV5lz').click()
    print("Clicked")

    # Sign in button css selector
    selector = '/html/body/div[4]/div[2]/div/div[2]/div[2]/div/div'
    wait.until(ec.presence_of_element_located((By.XPATH, selector)))
    wait.until(ec.element_to_be_clickable((By.XPATH, selector)))
    driver.find_element(By.XPATH, selector).click()

    print('Clicked Sign In')

    try:
        # other sign in options css selector
        selector = 'a.scene-login-icon-more'
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, selector)))
        wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        driver.find_element(By.CSS_SELECTOR, selector).click()
        print('Clicked Others option')

        # sign in button css selector
        selector = '/html/body/div[5]/div/div[2]/div/div[2]/div[1]/div[1]/div/div[2]'
        wait.until(ec.presence_of_element_located((By.XPATH, selector)))
        wait.until(ec.element_to_be_clickable((By.XPATH, selector)))
        driver.find_element(By.XPATH, selector).click()
        print('Clicked sign in again')

        # eamil filed id
        emali_field_id = 'fm-login-id'
        wait.until(ec.presence_of_element_located((By.ID, emali_field_id)))
        driver.find_element(By.ID, emali_field_id).send_keys(email)

        # password field id
        pass_field_id = 'fm-login-password'
        wait.until(ec.presence_of_element_located((By.ID, pass_field_id)))
        driver.find_element(By.ID, pass_field_id).send_keys(password)

        # sign in button css selector
        selector = '#batman-dialog-wrap > div > div.batman-msite > div > div.cosmos-tabs-container > div.cosmos-tabs-pane.cosmos-tabs-pane-active > div > button.cosmos-btn.cosmos-btn-primary.cosmos-btn-large.cosmos-btn-block.login-submit'
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, selector)))
        wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        driver.find_element(By.CSS_SELECTOR, selector).click()

        try:
            time.sleep(10)
            print("wait")
            WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div/div')))
            wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div/div')))
            driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div/div').click()
            time.sleep(15)
            driver.quit()
            return
        except Exception as e:
            print("err clicking help")
            raiseException(e)
        try:
            print("checking for captcha")
            WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'iframe#baxia-dialog-content')))
            iframe = driver.find_element(By.CSS_SELECTOR, 'iframe#baxia-dialog-content')
            if iframe.get_attribute('style').find('display: none;') == -1:
                print("Captcha Appeared")
                try:
                    driver.switch_to.frame(iframe)
                    # from bs4 import BeautifulSoup
                    # print(BeautifulSoup(driver.page_source, 'lxml').prettify())
                    WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CSS_SELECTOR, "span#nc_1_n1z")))
                    slider_container = driver.find_element(By.ID, "nc_1_wrapper")
                    slider = driver.find_element(By.CSS_SELECTOR, "span#nc_1_n1z")
                    print("selected")
                    # print("WIDTH: ", slider_container.size['width'])
                    # Perform sliding action
                    actions.move_to_element(slider).click_and_hold().move_by_offset(slider_container.size['width'], 0).release().perform()
                    driver.switch_to.default_content()
                    time.sleep(5)
                except Exception as e:
                    raiseException(e)
        except Exception as e:
            print("Cheking verification")
            wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '.fm-dialog-content iframe')))
            iframe = driver.find_element(By.CSS_SELECTOR, '.fm-dialog-content iframe')
            driver.switch_to.frame(iframe)
            driver.find_element(By.ID, 'checkcode').send_keys('Hello')
            print('Asking for verification code :( ')
            time.sleep(2)
        print("waiting for get help")

    except:
        print("error")
        try:
            WebDriverWait(driver, 20).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div/div')))
            wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div/div')))
            driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div[2]/div/div').click()
            time.sleep(10)
            driver.quit()
            return
        except Exception as e:
            print("err clicking help")
            raiseException(e)


def waitForThread(delay, my_threads):
    time.sleep(delay)
    for t in my_threads:
        t.join()
        if t in my_threads:
            my_threads.remove(t)
    return


if __name__ == '__main__':
    howLong = int(input("How many time do you wanna run the script: "))
    threadCount = int(input("How many thread you wanna a run in a single run: "))

    driver_ready = getDriver(headless=True)
    driver_ready.quit()

    for i in range(howLong):
        accounts = [account.replace('\n', '') for account in open('aliAccount.txt', 'r', encoding='utf-8').readlines()]
        accountsToFetch = accounts[0:threadCount]

        accounts = accounts[threadCount:]
        # with open('aliAccount.txt', 'w', encoding='utf-8') as aliAccount:
        #     for account in accounts:
        #         aliAccount.write(account + '\n')
        #     aliAccount.close()
        #
        # with open('done.txt', 'a', encoding='utf-8') as doneText:
        #     for account in accountsToFetch:
        #         doneText.write(account + '\n')
        #     doneText.close()
        print(len(accountsToFetch))
        threads = []
        for account in accountsToFetch:
            email = account.split(':')[0]
            password = account.split(':')[-1]
            runThread = threading.Thread(target=main, args=[email, password])
            runThread.start()
            threads.append(runThread)
        waitForThread(2, threads)

