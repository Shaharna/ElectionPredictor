from selenium import webdriver
from time import sleep
import pickle


class DataCollector:

    usr = ''
    pwd = ''
    facebook_users = ['shahar.nahum.9', 'shahar.nahum.9', 'shahar.nahum.9', 'shahar.nahum.9', 'shahar.nahum.9']
    # all names were deleted from git due to privacy issues

    @staticmethod
    def collect():

        data = dict()

        driver = webdriver.Chrome(executable_path='/Users/shaharna/node_modules/chromedriver/bin/chromedriver')

        driver.get('https://www.facebook.com/')
        print("Opened facebook")
        sleep(1)

        username_box = driver.find_element_by_id('email')
        username_box.send_keys(DataCollector.usr)
        print("Email Id entered")

        password_box = driver.find_element_by_id('pass')
        password_box.send_keys(DataCollector.pwd)
        print("Password entered")

        login_box = driver.find_element_by_id('loginbutton')
        login_box.click()

        sleep(1)
        # input('Press anything to quit')

        for name in DataCollector.facebook_users:
            sleep(30)
            driver.get('https://www.facebook.com/%s/likes' % name)
            sleep(30)
            likes = driver.find_elements_by_class_name("fsl")
            last_size = len(likes)
            while len(likes) < 100:
                lenOfPage = driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                sleep(30)
                likes = driver.find_elements_by_class_name("fsl")
                if len(likes) == last_size:
                    break
                last_size = len(likes)

            likes_text = []

            for like in likes:
                likes_text.append(like.text)

            driver.get('https://www.facebook.com/%s/tv' % name)
            sleep(2)
            tv_shows = driver.find_elements_by_class_name("gx6")
            last_size = len(tv_shows)
            while len(tv_shows) < 100:
                lenOfPage = driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                sleep(1)
                tv_shows = driver.find_elements_by_class_name("gx6")
                if len(tv_shows) == last_size:
                    break
                last_size = len(tv_shows)

            tv_shows_text = []

            for tv_show in tv_shows:
                tv_shows_text.append(tv_show.text)


            driver.get('https://www.facebook.com/%s/map' % name)
            sleep(2)
            check_ins = driver.find_elements_by_class_name("gx6")
            last_size = len(check_ins)
            while len(check_ins) < 100:
                lenOfPage = driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                sleep(1)
                check_ins = driver.find_elements_by_class_name("gx6")
                if len(check_ins) == last_size:
                    break
                last_size = len(check_ins)

            check_ins_text = []

            for check_in in check_ins:
                check_ins_text.append(check_in.text)

            data[name] = likes_text + tv_shows_text + check_ins

            driver.get('https://www.facebook.com/%s/music' % name)
            sleep(2)
            music = driver.find_elements_by_class_name("gx6")
            last_size = len(music)
            while len(music) < 100:
                lenOfPage = driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                sleep(1)
                check_ins = driver.find_elements_by_class_name("gx6")
                if len(music) == last_size:
                    break
                last_size = len(music)

            music_text = []

            for channel in music:
                music_text.append(channel.text)

            data[name] = likes_text #+ tv_shows_text + check_ins + music_text

        pickle_out = open("dict_all.pickle", "wb")
        pickle.dump(data, pickle_out)
        pickle_out.close()

        print("Done")
        input('Press anything to quit')
        driver.quit()
        print("Finished")
