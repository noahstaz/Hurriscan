import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPredictionsDashboard(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/predictions-dashboard")
    
    def test_make_prediction_button(self):
        map_element = self.driver.find_element(By.ID, "map")
        map_element.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "latitude")) and
            EC.presence_of_element_located((By.ID, "longitude"))
        )

        latitude_input = self.driver.find_element(By.ID, "latitude")
        longitude_input = self.driver.find_element(By.ID, "longitude")

        self.assertNotEqual(latitude_input.get_attribute("value"), "")
        self.assertNotEqual(longitude_input.get_attribute("value"), "")
        
    def test_select_map_spot(self):
        map_element = self.driver.find_element(By.ID, "map")
        map_element.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "latitude")) and
            EC.presence_of_element_located((By.ID, "longitude"))
        )

        latitude_input = self.driver.find_element(By.ID, "latitude")
        longitude_input = self.driver.find_element(By.ID, "longitude")
        latitude_value = latitude_input.get_attribute("value")
        longitude_value = longitude_input.get_attribute("value")

        self.assertNotEqual(latitude_value, "")
        self.assertNotEqual(longitude_value, "")
        
    def test_click_checkboxes(self):
        north_america_checkbox = self.driver.find_element(By.ID, "north-america")
        north_america_checkbox.click()

        south_america_checkbox = self.driver.find_element(By.ID, "south-america")
        south_america_checkbox.click()

        self.assertTrue(north_america_checkbox.is_selected())
        self.assertTrue(south_america_checkbox.is_selected())
        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
