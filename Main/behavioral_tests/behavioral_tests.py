from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
import time

#Opens a browser and logs into the test account on the website
def login_setup():
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

#Tests login with correct login information
def correct_login():
	driver = login_setup()

	login_status = driver.find_elements_by_id('login_status')

	if len(login_status) == 1:
		print("Correct Login Passed ")
		return 1
	else:
		print("Correct Login Failed ")
		return 0

	driver.quit()

#Tests login with incorrect login information
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

	driver.quit()

#Submits text to algorithm and checks to see if it was handled properly
def submit_and_check(temp_driver, num, algo):
	driver = temp_driver
	driver.find_element_by_id('submitbuttoninput').click()
	results = driver.find_element_by_id('resultscontents')
	msg = results.find_element_by_tag_name('p')
	if msg.text == "You didn't enter any text or files!":
		num = 1
	else:
		num = 0

	return num

#Tests TF-IDF when supplied text
def tfidf_test_text():
	num = 2
	algo = "TF-IDF"
	driver = login_setup()
	textbox = driver.find_element_by_name('textInput')
	textbox.send_keys("This is some sample text for the behavioral test")
	num = submit_and_check(driver, num, algo)
	if num == 0:
		driver.quit()
		print(algo + " handled text as expected.")
		return 1
	else:
		driver.quit()
		print(algo + " detected an error given text.")
		return 0

#Tests TF-IDF when supplied no text
def tfidf_test_no_text():
	num = 2
	algo = "TF-IDF"
	driver = login_setup()
	num = submit_and_check(driver, num, algo)
	if num == 1:
		driver.quit()
		print(algo + " handled no text as expected.")
		return 1
	else:
		driver.quit()
		print(algo + " detected an error given no text.")
		return 0

#Tests LDA when supplied text
def lda_test_text():
	num = 2
	algo = "LDA"
	driver = login_setup()
	select = Select(driver.find_element_by_id('algorithm'))
	select.select_by_index(1)
	textbox = driver.find_element_by_name('textInput')
	textbox.send_keys("This is some sample text for the behavioral test")
	num = submit_and_check(driver, num, algo)
	if num == 0:
		driver.quit()
		print(algo + " handled text as expected.")
		return 1
	else:
		driver.quit()
		print(algo + " detected an error given text.")
		return 0

#Tests LDA when supplied no text
def lda_test_no_text():
	num = 2
	algo = "LDA"
	driver = login_setup()
	select = Select(driver.find_element_by_id('algorithm'))
	select.select_by_index(1)
	num = submit_and_check(driver, num, algo)
	if num == 1:
		driver.quit()
		print(algo + " handled no text as expected.")
		return 1
	else:
		driver.quit()
		print(algo + " detected an error given no text.")
		return 0


#Tests POS when supplied text
def pos_test_text():
	num = 2
	algo = "POS"
	driver = login_setup()
	select = Select(driver.find_element_by_id('algorithm'))
	select.select_by_index(2)
	textbox = driver.find_element_by_name('textInput')
	textbox.send_keys("This is some sample text for the behavioral test")
	num = submit_and_check(driver, num, algo)
	if num == 0:
		driver.quit()
		print(algo + " handled text as expected.")
		return 1
	else:
		driver.quit()
		print(algo + " detected an error given text.")
		return 0


#Tests POS when supplied no text
def pos_test_no_text():
	num = 2
	algo = "POS"
	driver = login_setup()
	select = Select(driver.find_element_by_id('algorithm'))
	select.select_by_index(2)
	num = submit_and_check(driver, num, algo)
	if num == 1:
		driver.quit()
		print(algo + " handled no text as expected.")
		return 1
	else:
		driver.quit()
		print(algo + " detected an error given no text.")
		return 0

# create project tests?

#Runs all tests and tracks how many pass or fail
def test_suite():
	num_passed = correct_login() + incorrect_login() + tfidf_test_text() + \
	tfidf_test_no_text() + lda_test_text() + lda_test_no_text() + \
	pos_test_text() + pos_test_no_text()
	print("\n ... \n")
	print("Passed Tests: " , num_passed , "out of", 8)


test_suite()
