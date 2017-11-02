from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)

#navigate to the application home page
driver.get("https://www.nyse.com")

#get the search textbox
search_field = driver.find_element_by_css_selector("input[placeholder='Search']")
search_field.clear()

#enter search keyword and submit
search_item = "Willbros Group, Inc. (DE)"

search_to_match = re.sub('[^a-zA-Z]',' ',search_item)
search_to_match = ' '.join(search_to_match.split())
search_to_match = search_to_match.lower()

search_words = search_item.lower().split()
search_field.send_keys(search_item)
search_field.send_keys(Keys.RETURN)

#finding the results on the page
posts = driver.find_elements_by_class_name("search-results-title")
#storing all the results (the visible text) in a list
post_text = [post.text.lower() for post in posts]

#finding the text after the keyword to match with the search item
#we are doind this to find the link to be clicked
keyword = ':'
for item in post_text:
    if keyword in item:
        befor_keyword, keyword, after_keyword = item.partition(keyword)
        #removing all the characters and keeping only the alphabets
        after_keyword = re.sub('[^a-zA-Z]',' ',after_keyword)
        #removing extra spaces
        after_keyword = ' '.join(after_keyword.split())
        if search_to_match == after_keyword.lower():
            my_before_keyword = befor_keyword
            my_item = item

#we got the index of the link to be clicked
index = post_text.index(my_item)

#finding the link to be clicked
link_to_click = posts[index].find_element_by_css_selector('a').get_attribute('href')
#clicking on the link
driver.find_element_by_link_text(link_to_click).click()
#finding the trading time using Xpath
trad_time = driver.find_element_by_xpath("""/html/body/div[3]/div/div[4]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[3]/span[2]""")
print ("Entity :",my_before_keyword)
print ("trading time :",trad_time.text)
driver.quit()
