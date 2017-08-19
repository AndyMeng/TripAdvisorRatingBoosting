from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TRAVELLER_RATINGS= {
    "5":"taplc_location_review_filter_controls_hotels_0_filterRating_5",
    "4":"taplc_location_review_filter_controls_hotels_0_filterRating_4"
}

TRAVELLER_TYPES={
    "Families":"taplc_location_review_filter_controls_hotels_0_filterSegment_Families",
    "Couples":"taplc_location_review_filter_controls_hotels_0_filterSegment_Couples",
    "Solo":"taplc_location_review_filter_controls_hotels_0_filterSegment_Solo",
    "Business":"taplc_location_review_filter_controls_hotels_0_filterSegment_Business",
    "Friends":"taplc_location_review_filter_controls_hotels_0_filterSegment_Friends"
}

driver = webdriver.Firefox()

def game_start(ta_url):

    try:
        driver.get(ta_url)

        ## Filter reviews with 4 & 5 stars
        ##TODO 
        wait_for_element(driver.find_element_by_id(TRAVELLER_RATINGS["5"]))
        wait_for_element(driver.find_element_by_id(TRAVELLER_RATINGS["4"]))

        keys = list(TRAVELLER_TYPES)
        for key in keys:
            print("key: '"+key+"'\n")
            
            wait_for_element(driver.find_element_by_id(TRAVELLER_TYPES[key]))
            
            ## Expand all comments (both users' and hotel operator's)
            more_links = driver.find_elements(By.CSS_SELECTOR, 'span.taLnk.ulBlueLinks')
            if more_links:
                wait_for_element(more_links[0])
            
            review_containers = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')

            for container in review_containers:
                user = container.find_elements(By.CSS_SELECTOR, 'span.expand_inline.scrname')[0]
                user = user.text
                print(user+"\n")

            # Deselect the traveller type    
            wait_for_element(driver.find_element_by_id(TRAVELLER_TYPES[key]))

    except Exception as error:
        print("Web Driver exits unexpectedly with message: {0}".format(str(error)))
    finally:
        driver.quit()


def wait_for_element(option,  delay=2):
        option.click()
        WebDriverWait(driver, delay).until(EC.staleness_of(option))
    

def main():
    game_start('https://www.tripadvisor.com.sg/Hotel_Review-g294264-d1447339-Reviews-Hard_Rock_Hotel_Singapore-Sentosa_Island.html')

if __name__== "__main__":
    main()