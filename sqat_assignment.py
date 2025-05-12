import csv
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class UserData:
    def __init__(self, first_name, last_name, address, city, state, zip_code, phone, ssn, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.ssn = ssn
        self.username = username
        self.password = password

def log_report(logs, message):
    logs.append(f"<p>{message}</p>")
    print(message)

def open_url(driver, logs, url):
    log_report(logs, "Tanmoy Chandra Shill")
    driver.get(url)
    time.sleep(1)
    driver.maximize_window()
    log_report(logs, f"Opened URL: {url}")

def register_user(driver, logs, user):
    driver.find_element(By.LINK_TEXT, "Register").click()
    time.sleep(1)

    driver.find_element(By.ID, "customer.firstName").send_keys(user.first_name)
    log_report(logs, f"Type first name {user.first_name} into First Name field")

    driver.find_element(By.ID, "customer.lastName").send_keys(user.last_name)
    log_report(logs, f"Type last name {user.last_name} into Last Name field")

    driver.find_element(By.ID, "customer.address.street").send_keys(user.address)
    log_report(logs, f"Type address {user.address} into Address field")

    driver.find_element(By.ID, "customer.address.city").send_keys(user.city)
    log_report(logs, f"Type city {user.city} into City field")

    driver.find_element(By.ID, "customer.address.state").send_keys(user.state)
    log_report(logs, f"Type state {user.state} into State field")

    driver.find_element(By.ID, "customer.address.zipCode").send_keys(user.zip_code)
    log_report(logs, f"Type zip code {user.zip_code} into Zip Code field")

    driver.find_element(By.ID, "customer.phoneNumber").send_keys(user.phone)
    log_report(logs, f"Type phone number {user.phone} into Phone Number field")

    driver.find_element(By.ID, "customer.ssn").send_keys(user.ssn)
    log_report(logs, f"Type SSN {user.ssn} into SSN field")

    driver.find_element(By.ID, "customer.username").send_keys(user.username)
    log_report(logs, f"Type username {user.username} into Username field")

    driver.find_element(By.ID, "customer.password").send_keys(user.password)
    driver.find_element(By.ID, "repeatedPassword").send_keys(user.password)
    log_report(logs, f"Type password into Password and Confirm Password fields")

    driver.find_element(By.CSS_SELECTOR, "#customerForm input[type='submit']").click()
    time.sleep(1)
    log_report(logs, "User registered successfully")

def logout(driver, logs):
    driver.find_element(By.LINK_TEXT, "Log Out").click()
    time.sleep(1)
    log_report(logs, "Logout successfully")

def perform_login(driver, logs, username, password):
    driver.find_element(By.NAME, "username").send_keys(username)
    log_report(logs, f"Type username {username} into Username field")

    driver.find_element(By.NAME, "password").send_keys(password)
    log_report(logs, f"Type password into Password field")

    driver.find_element(By.CSS_SELECTOR, "#loginPanel input[type='submit']").click()
    time.sleep(1)
    log_report(logs, "Clicked Submit button")

def validate_login(driver, logs):
    try:
        driver.find_element(By.LINK_TEXT, "Log Out")
        log_report(logs, "Login successfully")
    except NoSuchElementException:
        log_report(logs, "Login failed")

def main():
    driver = webdriver.Chrome()
    logs = []
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"D:/ReportResult/Report_{date_str}.html"
    
    try:
        open_url(driver, logs, "https://parabank.parasoft.com/parabank/index.htm")

        with open("D:/UserData/UserData.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = UserData(
                    row['FirstName'], row['LastName'], row['Address'], row['City'],
                    row['State'], row['ZipCode'], row['Phone'], row['SSN'],
                    row['Username'], row['Password']
                )
                register_user(driver, logs, user)
                logout(driver, logs)
                perform_login(driver, logs, user.username, user.password)
                validate_login(driver, logs)

    except Exception as e:
        log_report(logs, f"<b>Test failed with exception:</b> {str(e)}")
    finally:
        driver.quit()
        with open(report_path, "w") as report_file:
            report_file.write("<html><body>" + "\n".join(logs) + "</body></html>")
        print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()
