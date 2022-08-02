from selenium import webdriver
import time


class TinderBot():
    def __init__(self,username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.url='https://tinder.com'


    def get_driver(self):
        driver=self.driver
        driver.implicitly_wait(10)
        driver.get(self.url)

    def login(self):
        self.get_drive()
        fb_btn = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')
        fb_btn.click()

        # switch to login popup
        base_window = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(self.username)
        time.sleep(2)
        pw_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pw_in.send_keys(self.password)
        time.sleep(2)

        login_btn = self.driver.find_element_by_xpath('//*[@id="u_0_0"]').click()

        self.driver.switch_to_window(base_window)
        popup_1 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
        popup_2 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()


    def like(self):
        like_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]')
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]')
        dislike_btn.click()

    def auto_swipe(self, percent):
        like_count=0
        dislike_count=0
        while True:
            time.sleep(0.5)
            if like_count/(like_count + dislike_count)*100 <= int(percent):
                try:
                    self.like()
                except Exception:
                    try:
                        self.close_popup()
                    except Exception:
                        self.close_match()
            else:
                try:
                    self.dislike()
                except Exception:
                    try:
                        self.close_popup()
                    except Exception:
                        self.close_match()

    def close_popup(self):
        popup_3 = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]').click()

    def close_match(self):
        match_popup = self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a').click()

    
#input username and password
bot = TinderBot(username, password)
bot.login()
#input like percentage
bot.auto_swipe(70)
