from time import time
from selenium import webdriver

CHROME_PATH = "YOUR CHROMEDRIVER PATH"
# set web and drive
driver = webdriver.Chrome(executable_path=CHROME_PATH)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# cookie variables
cookie = driver.find_element_by_id("cookie")
divs_array = driver.find_elements_by_css_selector("#store div")
divs_ids = [item.get_attribute("id") for item in divs_array]
timeout = time() + 5

# main loop
while True:
    # clicking cookie
    cookie.click()

    # every 5 sec
    if time() > timeout:

        # get <b>'s
        all_prices = driver.find_elements_by_css_selector("#store b")
        all_prices.pop()
        items_prices = []
        # converting to price
        for price in all_prices:
            cost = (price.text.split("-")[1].replace(",", ""))
            items_prices.append(int(cost))

        # current state of money
        tmp_money = driver.find_element_by_id("money").text
        if "," in tmp_money:
            tmp_money = tmp_money.replace(",", "")
        money = int(tmp_money)

        # finding upgrades that we can afford
        affordable_upgrades = {}
        for price in items_prices:
            if money > price:
                affordable_upgrades[items_prices.index(price)] = divs_ids[items_prices.index(price)]

        # highest affordable id
        highest_affordable = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_affordable]
        driver.find_element_by_id(to_purchase_id).click()

        # adds another 5 sec
        timeout = time() + 5
