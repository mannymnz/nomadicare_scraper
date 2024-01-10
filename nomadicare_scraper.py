import pdb
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get("https://www.nomadicare.com/licensure-guide/")


def get_data(driver):
    insurances = driver.find_elements(By.CLASS_NAME, "fwpl-result")
    results = []
    for insurance in insurances:
        lines = insurance.text.split("\n")
        state = lines[0].split(" ")[-1]
        license_type = " ".join(lines[0].split(" ")[:-2])
        
        info = {}
        info["state"] = state
        info["license_type"] = license_type
        for line in lines[1:]:
            [key, val] = line.split(": ")
            info[key] = val
        results.append(info)
    

    with open('nomadicare_insurance_data.json', 'w') as fp:
        json.dump(results, fp, indent=2)


still_more = True
while still_more:
    try:
        elements = driver.find_elements(By.CLASS_NAME, "facetwp-load-more")

        insurances = driver.find_elements(By.CLASS_NAME, "fwpl-result")
        print(len(insurances))
        if len(insurances) == 255:
            get_data(driver)
            break
            
        if len(elements) > 0 and elements[0].text == "Show more":
            elements[0].click()

        if len(elements) > 0 and not elements[0].is_displayed:
            still_more = False
        
    except:
        print("exception occurred")

