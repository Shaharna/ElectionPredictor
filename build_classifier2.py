import pandas as pd
from sklearn import neighbors
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from selenium import webdriver
from time import sleep
import pickle
from sklearn.tree import DecisionTreeClassifier
import re


# usr = 'shahar.nahum@mail.huji.ac.il'
# pwd = 'shahar1162016'

usr = 'shahar_na@walla.com'
pwd = 'shahar1162019'


def load_data():
    """

    :return:
    """
    data = dict()
    # with open("dict.pickle", "rb") as pickle_out:
    #     data = pickle.load(pickle_out)
    # with open("dict_2.pickle", "rb") as pickle_out:
    #     data.update(pickle.load(pickle_out))
    with open("dict_all.pickle", "rb") as pickle_out:
        data.update(pickle.load(pickle_out))
    return data


def process_data():
    """

    :return:
    """
    my_dict = load_data()
    df = pd.DataFrame()
    for lst in my_dict.values():
        for like in lst:
            temp = []
            if like not in df.columns.tolist():
                for person_likes in my_dict.values():
                    if like in person_likes:
                        temp.append(1)
                    else:
                        temp.append(0)
                df[like] = temp
    return df

def filter_function(str):
    """

    :param str:
    :return:
    """
    prog = re.compile('Mutual Friend|Mutual Friends| Unnamed:')
    if prog.search(str):
        return True
    else:
        return False

def filter_page(str):
    """

    :param str:
    :return:
    """
    prog = re.compile('/mutual_friends/|browse|uid')
    if prog.search(str):
        return True
    else:
        return False

def predict(name):
    """

    :param value:
    :return:
    """
    # extract_likes(name)
    test = extract_likes(name)

    df = pd.read_csv('test.csv')
    labels = df['labels']
    df = df.drop(columns=['labels', 'binary labels', 'To see what he shares with friends, send him a friend request.'])
    df = df.dropna(axis=1)
    lst = filter(filter_function, df.columns.tolist())
    print(lst)
    df = df.drop(columns=lst)

    # svc_classifier = LinearSVC()
    # forest = RandomForestClassifier()
    # log = LogisticRegression()
    # knn = neighbors.KNeighborsClassifier(n_neighbors=1)
    d_tree = DecisionTreeClassifier()

    # svc_classifier.fit(df, labels)
    # forest.fit(df, labels)
    # log.fit(df, labels)
    # knn.fit(df, labels)
    d_tree.fit(df, labels)

    test_x = pd.DataFrame()

    for page in df.columns.tolist():

        page_col = []

        for test_lst in test.values():

            if page in test_lst:

                page_col.append(1)
            else:
                page_col.append(0)

        test_x[page] = page_col

    test_x.to_csv('results.csv')

    tags = (d_tree.predict(test_x[0:]))

    print(tags)

    votes = count_votes(tags)

    plt.title("Your friends votes")
    plt.pie(x=votes.values(), labels=votes.keys())
    plt.show()


def extract_likes(name):
    """

    :param name:
    :return:
    """
    driver = webdriver.Chrome(
        executable_path='/Users/shaharna/node_modules/chromedriver/bin/chromedriver')
    driver.get('https://www.facebook.com/')
    print("Opened facebook")
    sleep(1)
    username_box = driver.find_element_by_id('email')
    username_box.send_keys(usr)
    print("Email Id entered")
    password_box = driver.find_element_by_id('pass')
    password_box.send_keys(pwd)
    print("Password entered")
    login_box = driver.find_element_by_id('loginbutton')
    login_box.click()
    driver.get('https://www.facebook.com/%s/friends' % name)
    friends = driver.find_elements_by_class_name("_39g5")
    last_size = len(friends)
    while len(friends) < 100:
        print(len(friends))
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        sleep(20)
        friends = driver.find_elements_by_class_name("_39g5")

        if len(friends) == last_size:
            print(last_size, len(friends))
            break
        last_size = len(friends)

    # driver.close()
    friends_text = []
    #
    for friend in friends:
        friends_text.append(str(friend.get_attribute('href')).replace("/friends", ""))


    print(friends_text)
    return extract_all_likes(driver, friends_text)


def extract_all_likes(driver, friends):
    """

    :param driver:
    :param name:
    :return:
    """
    data = dict()
    for friend in friends:
        sleep(10)
        url = "%s/likes" %str(friend)
        driver.get(url)
        if (driver.current_url != friend) and not(bool(re.search('browse|mutual_friends', str(driver.current_url)))):
            likes = driver.find_elements_by_class_name("fsl")
            last_size = len(likes)
            while len(likes) < 100:
                lenOfPage = driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                sleep(20)
                likes = driver.find_elements_by_class_name("fsl")
                if len(likes) == last_size:
                    break
                last_size = len(likes)

            likes_text = []

            for like in likes:
                likes_text.append(like.text)

            data[friend] = likes_text

    driver.close()

    return data


def mostFrequent(arr, n):
    # Sort the array
    arr.sort()

    # find the max frequency using
    # linear traversal
    max_count = 1
    res = arr[0]
    curr_count = 1

    for i in range(1, n):
        if (arr[i] == arr[i - 1]):
            curr_count += 1

        else:
            if (curr_count > max_count):
                max_count = curr_count
                res = arr[i - 1]

            curr_count = 1

    # If last element is most frequent
    if (curr_count > max_count):
        max_count = curr_count
        res = arr[n - 1]

    return res

def count_votes(arr):
    """

    :param arr:
    :return:
    """
    votes = dict()
    for vote in arr:

        if vote in votes.keys():
            votes[vote] += 1
        else:
            votes[vote] = 1

    return votes