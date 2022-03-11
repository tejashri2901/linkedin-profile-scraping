# importing required packages
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# paste ur email id and password in double quotes
password = "Password"
email = "email@gmail.com"
# t = maximum time to scroll page (differs with content of page) and stability of internet
# l = max time it should wait to load the section
def scroll(t, l, driver):
    start = time.time()

    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000

    while True:
        # scrolling page to 1000 px every time loop runs
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000
        time.sleep(l)
        end = time.time()
        if round(end - start) > t:
            break
# Initialising lists for collecting content of different attributes
connect = []  # list for storing connections link
mutuals = []   # list for storing count of mutual connection and we have
name = []   # list for storing names of connections
roll = []   # list for storing roll they are currently playing
skills = []   # list for storing list of skills a connection have
location = []   # list for storing current location of connection
conn_member_have = []   # list for storing total number of connections a connection have
about = []   # list for storing their about data
experience_list = []   # list for storing list of experience they gained till now
education = []   # list for storing education of connection
emails = []   # list for storing email address of connections

# filename to save csv file
filename = "sunny.csv"
# Making instance of Chrome browser
driver = webdriver.Chrome()
# going to login page
driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
driver.maximize_window()
# Below command stops the execution of program for that much seconds
time.sleep(3)
# selecting input field and filling required login details
driver.find_element(By.ID, "username").send_keys(email)
driver.find_element(By.ID, "password").send_keys(password)
# clicking sign in button leading us to home page
driver.find_element(By.XPATH, "//*[@id='organic-div']/form/div[3]/button").click()
# Using time.sleep() when required because sometimes browser takes time to load content
# Seconds pass varies with internet speed and loading of page
time.sleep(3)
# Below line lead us to connection page
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
time.sleep(3)
# saving page source code  in src variable
src = driver.page_source
# making instance of Beautifulsoup and using its methods
soup = BeautifulSoup(src, 'lxml')
# using scroll method in cvvvvvv to scroll the page ensuring complete loading of page
scroll(25, 3, driver)
try:
    # if number of connection is more then click the button named "Show more result"
    driver.find_element(By.XPATH,
                        "/html/body/div[5]/div[3]/div/div/div/div/div[2]/div/div/main/div/section/div[2]/div[2]/div/button").click()
    # and scroll it till end of list
    scroll(50, 3, driver)
except:
    scroll(30, 5, driver) # if such button is not found then simply scroll it for 30 seconds
time.sleep(2)
# finding all the links the page contains
kj = driver.find_elements(By.TAG_NAME, 'a')
time.sleep(4)
# filtering list to get only required links for preogra
for i in range(8, len(kj) - 8, 2):
    k = kj[i].get_attribute('href')
    connect.append(k)

# printing total number of connections we have and list of links of connections
print(len(connect), connect)
# headings of the columns to be given in csv file
tle = ['Sr No', 'NAME', 'ROLL', 'LOCATION', 'EMAIL','CONNECTIONS_THEY_HAVE', 'MUTUALS_WE_HAVE', "EDUCATION", "EXPERIENCE",
       'SKILLS', 'ABOUT']
# opening csv file with write mode
with open(filename, 'w', encoding='utf-8') as csvfile:
    # initialising writer to csv file
    csvwriter = csv.writer(csvfile)
    # appending heading row in  csv file
    csvwriter.writerow(tle)
    time.sleep(3)
    # looping through connect list one by one and fetching details of each section of profile separately
    # for now it will run for 4 profiles only
    # to run it for entire connections replace 4 with len(connect)
    # change start and end to any number to fetch details of only that connections
    # make sure start < end
    for l in range(0, 4):
        # visiting every link one-by-one
        driver.get(connect[l])
        # srolling through page
        scroll(10, 3, driver)
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        # finding header section
        header_divion = soup.find('div', class_='ph5 pb5')
        # name of connection
        try:
            name.append(
                header_divion.find('h1',
                                   class_='text-heading-xlarge inline t-24 v-align-middle break-words').text.strip())
        except:
            name.append('NULL')
        # roll of connection
        try:
            roll.append(header_divion.find('div', class_='text-body-medium break-words').text.strip())
        except:
            roll.append('NULL')
        # location of connection
        try:
            location.append(
                header_divion.find('span', class_='text-body-small inline t-black--light break-words').text.strip())
        # print(location)
        except:
            location.append('NULL')
        # total connections
        try:
            conn_member_have.append(
                header_divion.find('span', class_='link-without-visited-state').find('span',
                                                                                     class_='t-bold').text.strip())
        # print(conn_member_have)
        except:
            conn_member_have.append("NULL")
        # mutual connections
        try:
            mutuals.append(
                header_divion.find('span',
                                   class_='t-normal t-black--light t-14 hoverable-link-text').strong.text.strip())
        except:
            mutuals.append('NULL')
        # about section
        try:
            ab_drgr = soup.find('div', class_='display-flex ph5 pv3')
            about.append(ab_drgr.find('span', class_='visually-hidden').text.strip())
        except:
            about.append('NULL')
        # experience section
        try:

            ki = soup.find(string=['Experience']).find_parent('section')
            time.sleep(2)
            experience = ki.find_all('div',
                                     class_='pvs-entity pvs-entity--padded pvs-list__item--no-padding-when-nested')
            time.sleep(2)
            ji = []
            exxx = []
            for ele in experience:
                time.sleep(2)
                for i in ele.find_all('span', class_='visually-hidden'):
                    ji.append(i.text)
                exxx.append(ji.copy())
                ji.clear()
            experience_list.append(exxx.copy())
            exxx.clear()
        except:
            experience_list.append('NULL')
        # education section
        try:
            kit = soup.find(string=['Education']).find_parent('section')
            time.sleep(2)
            education_ = kit.find_all('div',
                                      class_='pvs-entity pvs-entity--padded pvs-list__item--no-padding-when-nested')
            time.sleep(2)
            jit = []
            edd = []
            for ele in education_:
                for i in ele.find_all('span', class_='visually-hidden'):
                    jit.append(i.text)
                edd.append(jit.copy())
                jit.clear()
            education.append(edd.copy())
            edd.clear()
        except:
            education.append('NULL')
            time.sleep(2)
        # contact info emails
        url = connect[l] + 'overlay/contact-info/'
        try:
            driver.get(url)
            time.sleep(2)
            s2 = driver.page_source
            code_soup = BeautifulSoup(s2, 'lxml')
            time.sleep(2)
            kp = code_soup.find('div', class_="artdeco-modal__content ember-view").find_all('a',
                                                                                            class_='pv-contact-info__contact-link link-without-visited-state t-14')
            time.sleep(2)
            email = kp[1].text.strip()
            emails.append(email)
        except:
            emails.append('NULL')
        # skills they have
        gett = str(connect[l]) + 'details/skills/'
        try:
            driver.get(gett)
            time.sleep(2)
            srds = driver.page_source
            soup1 = BeautifulSoup(srds, 'lxml')
            one_by_one = []
            time.sleep(2)
            for j in soup1.find_all('div',
                                    class_='pvs-entity pvs-entity--padded pvs-list__item--no-padding-when-nested'):
                hjh = j.find('span', class_='visually-hidden').text.strip()
                one_by_one.append(hjh)
            skills.append(one_by_one.copy())
            one_by_one.clear()
        except:
            skills.append('NULL')

        time.sleep(1)
    # tle = ['Sr No', 'NAME', 'ROLL','LOCATION','EMAIL','CONNECTIONS_THEY_HAVE','MUTUALS_WE_HAVE',"EDUCATION", "EXPERIENCE",'SKILLS', 'ABOUT']
        # storing each deatail of connection fetched in variable row sequentially
        row = [l + 1, name[l], roll[l], location[l],emails[l], conn_member_have[l], mutuals[l], education[l],
                   experience_list[l],
                   skills[l], about[l]]
        time.sleep(1)
        # appending row in csv file
        csvwriter.writerow(row)
        # just for assuring every profile is visited and scraped
        print("______" + str(l + 1) + "______")

driver.quit()