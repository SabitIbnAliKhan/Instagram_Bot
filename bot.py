from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os 
import time 
import configparser
import urllib.request
#from utilityMethods.utilityMethods import *
import time

class instagramBot: 


    def __init__(self, username, password):

        self.username = username 
        self.password = password 
        self.base_url='https://www.instagram.com'
        self.driver = webdriver.Chrome('chromedriver.exe')  


    def login(self):

        self.driver.get('{}/accounts/login/'.format(self.base_url))
        enter_username = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'username')))
        enter_username.send_keys(self.username)
        enter_password = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.NAME, 'password')))
        enter_password.send_keys(self.password)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div').click()


    def navigateUser(self,user):

        self.driver.get('{}/{}/'.format(self.base_url,user))


    def followUser(self,user):
        self.navigateUser(user)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]").click()
    
    

    def unfollowUser(self,user):
        self.navigateUser(user)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]').click()
 
    
    
    def downloadUserImages(self, user):
        self.navigateUser(user)
        imgSrcs = []
        finished = False 
        while not finished:
            finished = self.infiniteScroll()
            imgSrcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')]) 
        imgSrcs = list(set(imgSrcs))

        for idx, src in enumerate(imgSrcs):
            self.downloadImage(src, idx, user)


    def downloadImage(self, src, imgFileName, folder):
        folderPath = './{}'.format(folder)
        if not os.path.exists(folderPath):
            os.mkdir(folderPath)
        imgName = 'image_{}.jpg'.format(imgFileName)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, imgName))
      


    def infiniteScroll(self):

        SCROLL_PAUSE_TIME = 1
        self.lastHeight = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        self.newHeight = self.driver.execute_script("return document.body.scrollHeight")

        if self.newHeight == self.lastHeight:
            return True
        self.lastHeight = self.newHeight
        return False


    def likePosts(self,user,nPosts,like=True): 
        action = 'Like' if like else 'Unlike'

        self.navigateUser(user)
        imgs= []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))
        for img in imgs[:nPosts]:
            img.click()
            time.sleep(2)
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                print(e)
            self.driver.find_element_by_xpath("//*[@aria-label='Close']").click()
            time.sleep(2)
    


if __name__=='__main__':
    
    configPath ='./config_.ini'
    cParser= configparser.ConfigParser()
    cParser.read(configPath)
    user = cParser['IG_AUTH']['USERNAME']
    password = cParser['IG_AUTH']['PASSWORD']

    igBot = instagramBot(user, password)
    igBot.login()
    time.sleep(2)
    option = 0

    print("Select an option - 1 to follow user, 2 to unfollow user, 3 to Like n posts of user, 4 to Download user iamges, 5 to exit")

    while option != 5:
        option = int(input("Select an option: "))
           
        if option == 1: 
            name = input("Enter user to be followed: ")
            igBot.followUser(name)
            
        elif option == 2:
            name = input("Enter user to be unfollowed: ")
            igBot.unfollowUser(name)
           
        elif option == 3:
            name = input("Enter username: ")
            num = int(input("Enter number of posts to like"))
            igBot.likePosts(name, num) 

        elif option == 4: 
            name = input("Enter username: ")
            igBot.downloadUserImages(name)

        else: 
            print ("")
            
        
  
  