import time
import os
import sys
import time
import threading
from playwright.sync_api import Playwright, sync_playwright, expect

URL = 'https://a.aliexpress.com/_mMCaCy4'


def raiseException(err):
    print(err)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, file_name, exc_tb.tb_lineno)


class Tls(threading.local):
    def __init__(self) -> None:
        self.playwright = sync_playwright().start()
        print("Starting instances in Thread")


class Worker:
    tls = Tls()

    def run(self, username, password):
        pixel_2 = self.tls.playwright.devices['Pixel 2']
        browser = self.tls.playwright.webkit.launch(headless=False)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            viewport={'width': 480, 'height': 720}
        )
        page = context.new_page()
        page.goto(URL)

        page.wait_for_selector('//html/body/div[4]/div/div/div[2]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/div')
        page.locator('//html/body/div[4]/div/div/div[2]/div/div[2]/div/div/div[3]/div/div[2]/div[2]/div').click()

        page.wait_for_selector('//html/body/div[4]/div[2]/div/div[2]/div[2]/div/div', timeout=60000)
        time.sleep(1)
        page.locator('//html/body/div[4]/div[2]/div/div[2]/div[2]/div/div').click()

        page.wait_for_selector(
            'body > div:nth-child(18) > div.cosmos-drawer-wrap > div > div > div.cosmos-drawer-body > div > div.scene-login-other-icons > a.scene-login-icon-more')
        page.locator(
            'body > div:nth-child(18) > div.cosmos-drawer-wrap > div > div > div.cosmos-drawer-body > div > div.scene-login-other-icons > a.scene-login-icon-more').click()

        time.sleep(1)

        page.wait_for_selector('//*[@id="batman-dialog-wrap"]/div/div[2]/div[1]/div[1]/div/div[2]')
        page.locator('//*[@id="batman-dialog-wrap"]/div/div[2]/div[1]/div[1]/div/div[2]').click()

        page.wait_for_selector('#fm-login-id')
        page.locator('#fm-login-id').fill(username)
        page.wait_for_selector('#fm-login-password')
        page.locator('#fm-login-password').fill(password)
        time.sleep(2)

        page.wait_for_selector('//*[@id="batman-dialog-wrap"]/div/div[2]/div/div[2]/div[2]/div/button[2]')
        signin = page.locator('//*[@id="batman-dialog-wrap"]/div/div[2]/div/div[2]/div[2]/div/button[2]')
        signin.click()

        try:
            print('cheking if success')
            time.sleep(2)
            # Go help button
            go_help = '//html/body/div[4]/div/div/div[2]/div[2]/div/div'
            page.wait_for_selector(go_help, timeout=10000)
            page.locator(go_help).click()
            time.sleep(2)
            try:
                confirmBtn = '//html/body/div[4]/div/div/div[2]/div[2]/div/div[1]'
                print("checking confirm")
                page.wait_for_selector(confirmBtn)
                page.locator(confirmBtn).click()
            except Exception as e:
                print("Confirm button")
                page.close()
                context.close()
                return
        except:
            print('Not a success. Figuring out')
            try:
                page.wait_for_selector('//*[@id="batman-dialog-wrap"]/div/div[2]/div/div[2]/div[2]/div/div[4]/div[2]', timeout=10000)
                print(' Wrong Credentials')
                return
            except Exception as e:
                try:
                    page.wait_for_selector('//*[@id="batman-dialog-wrap"]/div/div[2]/div/div[2]/div[2]/div/div[4]/div[1]', timeout=10000)
                except Exception as e:
                    try:
                        page.wait_for_selector('//*[@id="batman-dialog-wrap"]/div/div[2]/div/div[2]/div[2]/div/div[3]/span', timeout=10000)
                        print('Cpatcha')
                        try:
                            print('Trying to solve..')
                            page.frame_locator('//*[@id="baxia-dialog-content"]')
                            frame_ = page.main_frame.child_frames[1]
                            frame_.wait_for_selector('//*[@id="nc_1_n1z"]')
                            box = frame_.locator('//*[@id="nc_1__scale_text"]/span')
                            # print(box.bounding_box())
                            slider = frame_.locator('//*[@id="nc_1_n1z"]')
                            # print(slider.bounding_box())
                            # slider.drag_to(target=box, target_position={'x': 500, 'y': box.bounding_box().get('y')})
                            frame_.drag_and_drop('//*[@id="nc_1_n1z"]', '//*[@id="nc_1_n1z"]', target_position={'x': 500, 'y': 66}, force=True)
                            time.sleep(3)
                            page.wait_for_selector('//*[@id="batman-dialog-wrap"]/div/div[2]/div/div[2]/div[2]/div/button[2]')
                            signin.click()
                            try:
                                go_help = '//html/body/div[4]/div/div/div[2]/div[2]/div/div'
                                page.wait_for_selector(go_help)
                                page.locator(go_help).click()
                                time.sleep(2)
                                confirmLocator = '//html/body/div[4]/div/div/div[2]/div[2]/div/div[1]'
                                page.wait_for_selector(confirmLocator)
                                page.locator(confirmLocator).click()
                                time.sleep(3)
                            except Exception as e:
                                print('Wrong Credentials')
                                page.close()
                                context.close()
                        except Exception as e:
                            raiseException(e)

                    except Exception as e:
                        print('Ok to go')
                        time.sleep(2)
                        # Go help button
                        go_help = '//html/body/div[4]/div/div/div[2]/div[2]/div/div'
                        page.wait_for_selector(go_help)
                        page.locator(go_help).click()
                        time.sleep(2)
                        try:
                            confirmLocator = '//html/body/div[4]/div/div/div[2]/div[2]/div/div[1]'
                            page.wait_for_selector(confirmLocator)
                            page.locator(confirmLocator).click()
                            time.sleep(3)
                        except Exception as e:
                            page.close()
                            context.close()

        time.sleep(5)
        page.close()
        context.close()


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

    for i in range(howLong):
        accounts = [account.replace('\n', '') for account in open('aliAccount.txt', 'r', encoding='utf-8').readlines()]
        accountsToFetch = accounts[0:threadCount]

        accounts = accounts[threadCount:]
        with open('aliAccount.txt', 'w', encoding='utf-8') as aliAccount:
            for account in accounts:
                aliAccount.write(account + '\n')
            aliAccount.close()

        with open('done.txt', 'a', encoding='utf-8') as doneText:
            for account in accountsToFetch:
                doneText.write(account + '\n')
            doneText.close()
        print(len(accountsToFetch))
        threads = []
        for account in accountsToFetch:
            email = account.split(':')[0]
            password = account.split(':')[-1]
            worker = Worker()
            runThread = threading.Thread(target=worker.run, args=[email, password])
            runThread.start()
            threads.append(runThread)
        waitForThread(2, threads)
