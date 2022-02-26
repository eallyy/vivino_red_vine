from selenium import webdriver
import time
import xlsxwriter

PATH = "/Users/eally/Desktop/chromedriver"
driver = webdriver.Chrome(PATH)

linkFile = open("collectedLinks.txt", "r")
linkList = linkFile.read().splitlines()
linkFile.close()

allDatas = [["winery", "wine", "wine_country", "wine_region", "wine_style", "grapes", "alcohol_content", "light_bold", "smooth_tannic", "dry_sweet", "soft_acidic", "high_note", "mid_note", "low_note", "rating", "rated_users"]]
startTime = time.time()
linkCounter = 1
linkListLen = len(linkList)

for link in linkList:
    driver.get(link)
    for height in range(0, 9000, 300):
        driver.execute_script(f"window.scrollTo(0, {height})")
        time.sleep(0.1)
    time.sleep(0.5)

    wineDatas = []

    # Get winery
    wineDatas.append(driver.find_element_by_class_name("winery").text)

    # Get wine
    wineDatas.append(driver.find_element_by_class_name("vintage").text)

    # Get wine country and region
    regionDatas = driver.find_elements_by_class_name("breadCrumbs__link--1TY6b")
    wineDatas.append(regionDatas[0].text) 
    wineDatas.append(regionDatas[1].text)

    # Get grapes, wine style and alcohol content.
    wine_style = ""
    wine_styleIndex = False
    grapes = ""
    grapesIndex = False
    alcohol_content = ""
    alcohol_contentIndex = False

    indexCursor = 0
    factHeaders = driver.find_elements_by_class_name("wineFacts__headerLabel--14doB")
    for factHeader in factHeaders:
        if factHeader.text == "Grapes":
            grapesIndex = indexCursor
        elif factHeader.text == "Wine style":
            wine_styleIndex = indexCursor
        elif factHeader.text == "Alcohol content":
            alcohol_contentIndex = indexCursor
        indexCursor += 1

    facts = driver.find_elements_by_class_name("wineFacts__fact--3BAsi")
    if wine_styleIndex:
        wine_style = facts[wine_styleIndex].text
    if grapesIndex:
        grapes = facts[grapesIndex].text
        if "% " in grapes:
            grapes = grapes.split("% ")[1]
        if "," in grapes:
            grapes = grapes.split(",")[0]
    if alcohol_contentIndex:
        alcohol_content = facts[alcohol_contentIndex].text.replace("%", "")
    
    wineDatas.append(wine_style)
    wineDatas.append(grapes)
    wineDatas.append(alcohol_content)

    # Taste points
    progressBars = driver.find_elements_by_css_selector("div.tasteStructure__progressBar--hjNb2 > span")
    wineDatas.append(round(float(progressBars[0].get_attribute("style").split(" ")[-1][:-2])*100/85))
    wineDatas.append(round(float(progressBars[1].get_attribute("style").split(" ")[-1][:-2])*100/85))
    wineDatas.append(round(float(progressBars[2].get_attribute("style").split(" ")[-1][:-2])*100/85))
    wineDatas.append(round(float(progressBars[3].get_attribute("style").split(" ")[-1][:-2])*100/85))

    driver.execute_script("window.scrollTo(0, 0)")

    # Get notes.
    driver.find_element_by_class_name("tasteNote__popularKeywords--1q7RG").click()
    allNotes = driver.find_elements_by_class_name("noteTag__name--CrZvX")
    time.sleep(0.5)
    for i in range(0,3):
        wineDatas.append(allNotes[i].text)
    driver.find_element_by_class_name("baseModal__closeContainer--1k7ov").click()

    driver.execute_script("window.scrollTo(0, 0)")
    # Get rating
    wineDatas.append(driver.find_element_by_class_name("vivinoRating__averageValue--3Navj").text)

    # Get rated users
    wineDatas.append(int(driver.find_element_by_class_name("vivinoRating__caption--3tZeS").text.split(" ")[0]))

    allDatas.append(wineDatas)
    print(str(linkCounter) + " link completed in " + str(linkListLen))
    linkCounter += 1

print(allDatas)

workbook = xlsxwriter.Workbook("red_wine_dataset.xlsx")
worksheet = workbook.add_worksheet()

row = 0
for wine in allDatas:
    worksheet.write(row, 0, wine[0])
    worksheet.write(row, 1, wine[1])
    worksheet.write(row, 2, wine[2])
    worksheet.write(row, 3, wine[3])
    worksheet.write(row, 4, wine[4])
    worksheet.write(row, 5, wine[5])
    worksheet.write(row, 6, wine[6])
    worksheet.write(row, 7, wine[7])
    worksheet.write(row, 8, wine[8])
    worksheet.write(row, 9, wine[9])
    worksheet.write(row, 10, wine[10])
    worksheet.write(row, 11, wine[11])
    worksheet.write(row, 12, wine[12])
    worksheet.write(row, 13, wine[13])
    worksheet.write(row, 14, wine[14])
    worksheet.write(row, 15, wine[15])
    row += 1
workbook.close()

print("Finished in: " + str(time.time() - startTime) + "seconds.")