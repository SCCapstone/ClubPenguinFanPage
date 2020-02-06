from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
import time

def setup():
	driver = webdriver.Chrome()
	driver.get("http://textpenguin.herokuapp.com/")

	login = driver.find_element_by_xpath('//a[@href="/accounts/login/"]')
	login.click()


	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "loginformbox")))
	time.sleep(1)

	email = driver.find_element_by_name('username')
	email.send_keys("clubpenguin")

	password = driver.find_element_by_name('password')
	password.send_keys("gamecocks")

	login_btn = driver.find_element_by_id('loginsubmit')
	login_btn.click()
	time.sleep(1)
	return driver


def teardown():
	driver.quit()


def correct_login():
	driver = setup()

	login_status = driver.find_elements_by_id('login_status')

	if len(login_status) == 1:
		print("Correct Login Passed ")
		return 1
	else:
		print("Correct Login Failed ")
		return 0

	teardown()


def incorrect_login():
	driver = webdriver.Chrome()
	driver.get("http://textpenguin.herokuapp.com/")

	login = driver.find_element_by_xpath('//a[@href="/accounts/login/"]')
	login.click()


	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "loginformbox")))
	time.sleep(1)

	email = driver.find_element_by_name('username')
	email.send_keys("wrong")

	password = driver.find_element_by_name('password')
	password.send_keys("verywrong")

	login_btn = driver.find_element_by_id('loginsubmit')
	login_btn.click()
	time.sleep(1)

	login_status = driver.find_elements_by_id('login_status')

	if len(login_status) == 1:
		print("Incorrect Login Failed ")
		return 0
	else:
		print("Incorrect Login Passed ")
		return 1

	teardown()


def test_suite():
	num_passed = correct_login() + incorrect_login()
	print("\n ... \n")
	print ("Passed Tests: " , num_passed , "out of", 2)



test_suite()
