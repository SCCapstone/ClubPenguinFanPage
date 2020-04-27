from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
import random
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



	buttons = driver.find_elements_by_class_name("nav-item")

	if len(buttons) == 5:
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

	buttons = driver.find_elements_by_class_name("nav-item")

	if len(buttons) == 5:
		print("Incorrect Login info detected an error.")
		return 0
	else:
		print("Incorrect Login info worked as expected. ")
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

#Tests if the user can create a project
def create_project_test():
	num = 0
	driver = login_setup()
	navlinks = driver.find_elements_by_class_name('nav-item')
	navlinks[1].click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, \
	"projectstuff")))
	time.sleep(1)
	driver.find_element_by_class_name("button").click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, \
	"firstdocinput")))
	time.sleep(1)
	title = driver.find_element_by_id("titleinput")
	title.send_keys("projecttest")
	body = driver.find_element_by_id("firstdocinput")
	body.send_keys("This is example input.")
	driver.find_element_by_id("submitbuttoninput").click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, \
	"flex-column")))
	time.sleep(1)
	projects = driver.find_elements_by_class_name("projectstuff")
	i = 0
	for n in projects:
		proj = projects[i].find_element_by_class_name("individualproject")
		title = proj.find_element_by_tag_name("h4")
		if title.text == "projecttest":
			driver.quit()
			num = 1
			print("Project successfully created.")
			return num
		i = i + 1

	driver.quit()
	print("Project failed to be created.")
	return num


#Tests to see if the user can delete a project
#NOTE: Run after create_project_test() or it will automatically fail!
#NOTE: This will delete all projects named "projecttest"!
def delete_project_test():
	num = 0
	driver = login_setup()
	navlinks = driver.find_elements_by_class_name('nav-item')
	navlinks[1].click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, \
	"projectstuff")))
	time.sleep(1)
	projects = driver.find_elements_by_class_name("projectstuff")
	i = 0
	for n in projects:
		proj = projects[i].find_element_by_class_name("individualproject")
		title = proj.find_element_by_tag_name("h4")
		if title.text == "projecttest":
			projects[i].find_element_by_class_name("deleteprojbutton").click()
			num = 1
			alert_obj = driver.switch_to.alert
			alert_obj.accept()
			print("Project successfully deleted.")
			driver.quit()
		i = i + 1

	if num == 0:
		driver.quit()
		print("Project failed to be deleted.")

	return num


#Tests bookmarklet functionality
def bookmarklet_test():
	driver = webdriver.Chrome()
	driver.get("https://www.npr.org/sections/coronavirus-live-updates/2020/04/25/844939777/no-evidence-that-recovered-covid-19-patients-are-immune-who-says")
	src = driver.find_element_by_class_name('credit-caption')
	dst = driver.find_element_by_tag_name('p')
	ActionChains(driver).drag_and_drop(src, dst).perform()

	js = """
	javascript:(function() {
		if(window.getSelection){
			var bookmarklet_text = window.getSelection();
			console.log("Selected Text: " + bookmarklet_text);
			window.location.href = "https://textpenguin.herokuapp.com/guesthome/" + "#" + bookmarklet_text;
		}
	})();

	"""
	driver.execute_script(js)
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "algorithm")))
	time.sleep(1)

	text = driver.find_element_by_tag_name("textarea")
	if text.text != "Input the text of document!":
		print("Bookmarklet sent text successfully.")
		driver.quit()
		return 1
	else:
		print("Bookmarklet didn't send text properly.")
		driver.quit()
		return 0

#Tests if a user can create a new account
def create_account_test():
	num = 0
	username = str(random.randint(1000000, 9999999))
	username = username + 'a'
	password = str(random.randint(1000000, 9999999))
	password = password + 'b'

	driver = webdriver.Chrome()
	driver.get("http://textpenguin.herokuapp.com/")

	login = driver.find_element_by_xpath('//a[@href="/accounts/login/"]')
	login.click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "loginformbox")))
	time.sleep(1)
	driver.find_element_by_id("addlink1").click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "id_username")))
	time.sleep(1)
	driver.find_element_by_id("id_username").send_keys(username)
	driver.find_element_by_id("id_password1").send_keys(password)
	driver.find_element_by_id("id_password2").send_keys(password)
	driver.find_element_by_tag_name("button").click()

	#Log in with new username/password to test if an account was created
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, \
	"loginformbox")))
	time.sleep(1)

	driver.find_element_by_name('username').send_keys(username)
	driver.find_element_by_name('password').send_keys(password)
	login_btn = driver.find_element_by_id('loginsubmit')
	login_btn.click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, \
	"algorithm")))
	time.sleep(1)

	buttons = driver.find_elements_by_class_name("nav-item")

	if len(buttons) == 5:
		driver.quit()
		print("Created account successfully.")
		num = 1
	else:
		driver.quit()
		print("Create account failed.")
		num = 0

	return num





#Runs all tests and tracks how many pass or fail
def test_suite():
	num_passed = correct_login() + incorrect_login() + tfidf_test_text() + \
	tfidf_test_no_text() + lda_test_text() + lda_test_no_text() + \
	pos_test_text() + pos_test_no_text() + create_project_test() + \
	delete_project_test() + bookmarklet_test() + create_account_test()
	print("\n ... \n")
	print("Passed Tests: " , num_passed , "out of", 12)


test_suite()
