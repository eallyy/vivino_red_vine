from selenium import webdriver
import time

def scrollDown(activeDriver):
    activeDriver.execute_script("window.scrollTo(0, window.scrollY+15000)")
    activeDriver.execute_script("window.scrollTo(0, window.scrollY-200)")

PATH = "/Users/eally/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)

# Opening vivino
driver.get("https://www.vivino.com/explore")
time.sleep(1)

# Changing shipping location
driver.find_element_by_class_name("simpleLabel__label--4j3ek").click()
time.sleep(1)
shipToCountries = driver.find_elements_by_class_name("shipToDropdown__itemLink--glwhY")
shipToCountries[-1].click()
time.sleep(1)

# Changing ratings
ratingButtons = driver.find_elements_by_class_name("radio__radioBtn--1tzgw")
ratingButtons[-1].click()
time.sleep(1)

# Changing sorting method
driver.find_element_by_xpath("/html/body/div[2]/div[4]/div/div/div[1]/div[2]/div").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[5]/div[3]/ul/li[6]").click()
time.sleep(1)

# Expanding the price range
# -95, -50 for 0$ - 15$ range.
# -70, 18 for 15$ - 21$ range.
# -38, 40 for 21$ - 30$ range.
# 0, 75 for 30$ - 40$ range.
# 15, 115 for 40$ - 50$ range.
# 30, 130 for 50$ - 70$ range.
# 60, 150 for 70$ - 110$ range.
# 120, 175 for 110$ - 300$ range.
# 180, 230 for 300$ - 500+$ range.

rightSlider = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[5]")
leftSlider = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[4]")
move = webdriver.ActionChains(driver)
move.click_and_hold(rightSlider).move_by_offset(180,0).release().perform()
time.sleep(1)
move.click_and_hold(leftSlider).move_by_offset(230,0).release().perform()
time.sleep(10)

# Loading all the wines by scrolling down the page (OPTIMIZE IT!!!!!!)
linksFile = open("collectedLinks.txt", "a")
linksCursor = 0

while True:
    scrollDown(driver)
    time.sleep(1.5)

    # Getting all the links of vines
    wineLinks = driver.find_elements_by_css_selector("div.wineCard__wineCardContent--3cwZt > a")
    for i in range(linksCursor, len(wineLinks)):
        try:
            linksFile.writelines(str(wineLinks[i].get_attribute("href") + "\n"))
        except:
            pass
    linksCursor = len(wineLinks)
