from os import pipe
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup, element
import csv 
from selenium.common.exceptions import NoSuchElementException
import requests
import pandas as pd
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument



PATH = "C:\webdrivers\chromedriver.exe"
browser = webdriver.Chrome(executable_path=PATH,chrome_options=options)
r=40 # r for range that showing when scroll comes to end how many times to click the show more button
# browser.set_window_size(1600,900)
headers_parameters = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}




# browser.get("https://www.linkedin.com/home")
# # browser.maximize_window()
# login_button=browser.find_element_by_xpath("/html/body/nav/div/a[2]")
# login_button.click()

# mail = browser.find_element_by_xpath("//*[@id='username']")
# password = browser.find_element_by_xpath("//*[@id='password']")

# mail.send_keys("")
# password.send_keys("")
# login_button1=browser.find_element_by_xpath("//*[@id='organic-div']/form/div[3]/button")

# login_button1.click()
# time.sleep(4)

browser.get("https://www.linkedin.com/jobs/search/?keywords=data%20scientist")

for x in range(1,8) :
   browser.execute_script('window.scrollTo(0,document.body.scrollHeight)') #for scrolling
   time.sleep(10)
time.sleep(20)


for x in range(1,r):#for show more button
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "infinite-scroller__show-more-button"))
            )
            element.click()
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)') 
            time.sleep(5)
        
        except:
            print("Can not find the button!!(Error)")



time.sleep(10)

time.sleep(5)
title_list=[]
company_list=[]
location_list=[]
time_list=[]
link_list=[]
content_list=[]
criteria_list=[]


job_lists = browser.find_element_by_class_name("jobs-search__results-list")
jobs = job_lists.find_elements_by_tag_name("li")

for element in jobs :
    


    
    job_title=element.find_element_by_css_selector("h3").get_attribute("innerText")
    job_company=element.find_element_by_css_selector("h4").get_attribute("innerText")
    job_location = element.find_element_by_class_name("job-search-card__location").text
    job_time = element.find_element_by_css_selector("time").get_attribute("datetime")
    job_link = element.find_element_by_css_selector("a").get_attribute("href")
    
    
      
    
    title_list.append(job_title)
    company_list.append(job_company)
    location_list.append(job_location)    
    time_list.append(job_time)
    link_list.append(job_link)

    
    x=0
for element in link_list : 
    
    try :
        profile_scrap=requests.get(element,headers=headers_parameters)
        profile =profile_scrap.content
    except requests.exceptions.ConnectionError: #Connection error try except block
        print("Connection Error")
        content_list.append("Empty")
        criteria_list.append("Empty")
        continue
    except requests.exceptions.ReadTimeout :
        print("Connection Error")
        content_list.append("Empty")
        criteria_list.append("Empty")
        continue
   
    try :
        profile_scrap.raise_for_status()
    except  requests.exceptions.HTTPError:#Http error try except block
        print("HTTP Error")
        content_list.append("Empty")
        criteria_list.append("Empty")
        continue
    x=x+1
    print(x)   

    # if profile_scrap.status_code!=200:
    #    continue 
    soup =BeautifulSoup(profile,"html.parser")
    profile_content = soup.find("div",{"class":"show-more-less-html__markup"})
    pr=profile_content.text
    content_list.append(" ".join(pr.split()))
    profile_criteria = soup.find_all("span",{"class":"description__job-criteria-text description__job-criteria-text--criteria"})
    txt = ""
    message = []
    for element in profile_criteria :
        txt = txt+element.text
    criteria_list.append(" ".join(txt.split()))

    


with open('Linkedin_last.csv','w',encoding="UTF-8",newline='') as f :
    headers = ["Title", "Company","Location","Time","Criteria","Link","Content"]
    writer = csv.DictWriter(f, delimiter="\t",fieldnames=headers)

    writer.writeheader()
    for x in range(len(jobs)):
#     thewriter.writerow([ title_list[x] , company_list[x] , location_list[x] , time_list[x],criteria_list[x] ,link_list[x] ,content_list[x]  ])
       
        writer.writerow({'Title': title_list[x], 'Company': company_list[x], 'Location': location_list[x],'Time':time_list[x],"Criteria":criteria_list[x],"Link":link_list[x],"Content":content_list[x]})



   







