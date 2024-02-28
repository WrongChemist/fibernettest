


# Chrome + Firefox
# config file (browser, browser version, run type, test types, NO AUTO-UPDATER)
# pytest
# Allure (reports)
# readme.md (setup, config, and execution)
# requirements.txt (Python packages)



# Rules:
# Pythhon 3.8
# Selenium
# pytest
# Git


# Key Features for Testing:
# 1. Product Browsing:
#  Navigate categories, search for products, view product details.
# 2. User Account Management:
#  Register for a new account, login/logout, access account
# dashboard.
# 3. Shopping Cart and Checkout:
#  Add products to cart, view cart, proceed through the checkout
# process.
# 4. Product Reviews:
#  Submit and view product reviews.



# Suggested Test Scenarios:
#  Verify navigation and product search functionality.
#  Test the registration, login, and logout processes.
#  Validate adding items to the cart, cart updates, and checkout process.
#  Ensure users can submit and view reviews on product pages.



# 1. Framework Infrastructure and Architecture:
#  Develop a test automation framework that is scalable and
# maintainable.
#  Use the Page Object Model (POM) pattern to ensure the
# maintainability of the test scripts.
#  Setup the framework to support tests on Chrome and Firefox
# browsers.
#  Utilize external configuration files for environment management.

# 2. Test Implementation:
#  Write functional tests covering user authentication, plan management,
# profile updates, and billing operations.
#  Include non-functional tests for performance benchmarks and basic
# security checks.
#  Ensure cross-browser testing capability.
#  Integrate pytest for test management and execution.

# 3. Reporting and Documentation:
#  Integrate a reporting tool like Allure to generate test execution reports.
#  Provide a README file with detailed setup and execution instructions,
# including environment setup, test execution, and report generation.

# 4. Code Management and Submission:
#  Initialize a Git repository for your project and make regular commits to
# demonstrate your progress.
#  Host your project on GitHub, making sure the repository is public so it
# can be reviewed by the Fibernet team.
#  Ensure your repository contains a clear and structured README.md
# file that guides the reviewer through setting up, running tests, and
# understanding your test framework.





import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import ActionChains as ac

from re import sub
from decimal import Decimal
from random import randint, shuffle
from math import isclose
import time
from time import localtime, strftime
import configparser
from pathlib import Path





class Test_fibernetSite():
    driver_path_chrome = ""
    driver_path_firefox = ""
    driver_exe_firefox = ""
    driver = None
    browser = ""
    site_address = ""

    store_categories_top = 0
    store_subcategories_top = []

    store_categories_in = 0
    store_subcategories_in = []

    user_first_name = ""
    user_last_name = ""
    user_mail = ""
    user_password = ""



    def test_config(self):
        config = configparser.ConfigParser()
        config.read('fbrntConfig.ini')
        config.sections()

        Test_fibernetSite.driver_path_chrome = config['Main']['Driver_Path_Chrome']
        Test_fibernetSite.driver_path_firefox = config['Main']['Driver_Path_Firefox']
        Test_fibernetSite.driver_exe_firefox = config['Main']['Driver_Exe_Firefox']
        Test_fibernetSite.driver_exe_firefox = (r'%s' % Test_fibernetSite.driver_exe_firefox)

        Test_fibernetSite.browser = config['Main']['browser'].lower()
        if Test_fibernetSite.browser == "chrome":
            gcoptions = webdriver.ChromeOptions()
            gcoptions.add_argument("start-maximized")
            gcservice = Service(executable_path=Test_fibernetSite.driver_path_chrome)
            Test_fibernetSite.driver = webdriver.Chrome(options=gcoptions, service=gcservice)
        elif Test_fibernetSite.browser == "firefox":
            ffoptions = webdriver.FirefoxOptions()
            ffoptions.add_argument("--start-maximized")
            ffoptions.binary = FirefoxBinary(Test_fibernetSite.driver_exe_firefox)
            ffservice = Service(executable_path=Test_fibernetSite.driver_path_firefox)
            Test_fibernetSite.driver = webdriver.Firefox(options=ffoptions, service=ffservice)

        Test_fibernetSite.driver.implicitly_wait(15)

        Test_fibernetSite.site_address = config['Addresses']['Site_Address']

        Test_fibernetSite.user_first_name = config['User']['User_First_Name']
        Test_fibernetSite.user_last_name = config['User']['User_Last_Name']
        Test_fibernetSite.user_mail = config['User']['User_Mail']
        Test_fibernetSite.user_password = config['User']['User_Password']



    def test_setup(self):
        self.driver = Test_fibernetSite.driver
        self.driver.maximize_window()
        self.driver.get(Test_fibernetSite.site_address)
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//nav[@id="top"]//span[contains (text(), "Account")]')))
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")]')))
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[contains (@class, "carousel")]//div[contains (@class, "carousel-item")]')))
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//footer//a')))
        time.sleep(10)



    def test_navigation_topstore(self):
        store_categories = 0
        store_type = ""
        store_subcategories = 0
        target_page_name = ""

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="narbar-menu"]//li')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="narbar-menu"]//li')))

        while True:
            try:
                self.driver.find_element(By.XPATH, '//div[@id="narbar-menu"]//li[%d]' % (store_categories + 1))
                store_categories = store_categories + 1
            except NoSuchElementException:
                break

        for x in range (1, store_categories + 1):
            store_subcategories = 0
            store_type = ""
            store_type = self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x).get_attribute("class")

            if store_type == "nav-item dropdown":
                self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x).click()
                while True:
                    try:
                        self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]//li[%d]/a' % (x, store_subcategories + 1))
                        store_subcategories = store_subcategories + 1
                    except NoSuchElementException:
                        break

                for y in range (1, store_subcategories + 1):
                    self.driver.find_element(By.XPATH,'//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x).click()
                    target_page_name = ((self.driver.find_element(By.XPATH,'//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]//li[%d]/a' % (x, y)).get_attribute("text")).split(" ("))[0]
                    self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]//li[%d]' % (x, y)).click()
                    target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h2'))).text
                    target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//aside[@id="column-left"]//a[contains (@class, "active")]'))).text

                self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x).click()
                target_page_name = self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]/a' % x).get_attribute("text")
                self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]/div/a' % x).click()
                target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h2'))).text
                target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//aside[@id="column-left"]//a[contains (@class, "active")]'))).text

            elif store_type == "nav-item":
                target_page_name = self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[%d]/a' % x).get_attribute("text")
                self.driver.find_element(By.XPATH, '//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x).click()
                target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h2'))).text
                target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//aside[@id="column-left"]//a[contains (@class, "active")]'))).text

            Test_fibernetSite.store_subcategories_top.append(store_subcategories)
        Test_fibernetSite.store_categories_top = store_categories



    def test_navigation_carousel(self):
        carousel_items = 0
        target_page_name = ""

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[contains (@class, "carousel")]//div[contains (@class, "carousel-item")]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[contains (@class, "carousel")]//div[contains (@class, "carousel-item")]')))

        while True:
            try:
                self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="carousel-indicators"]/button[%d]' % (carousel_items + 1))
                carousel_items = carousel_items + 1
            except NoSuchElementException:
                break

        for x in range (1, carousel_items + 1):
            target_page_name = self.driver.find_element(By.XPATH, '//div[@id="common-home"]//div[@class="carousel-inner"]/div[%d][contains (@class, "carousel-item active")]//img' % x).get_attribute("alt")
            self.driver.find_element(By.XPATH, '//div[@id="common-home"]//div[@class="carousel-indicators"]//button[%d]' % x).click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//div[@id="common-home"]//div[@class="carousel-inner"]/div[%d]' % x).click()
#            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="carousel-inner"]/div[%d][@class="carousel-item active"]' % x))).click()

            target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h1'))).text
            time.sleep(5)
            self.driver.get(Test_fibernetSite.site_address)
#            self.driver.find_element(By.XPATH, '//div[@id="logo"]/a').click()
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[contains (@class, "carousel")]//div[contains (@class, "carousel-item")]')))



    def test_navigation_featured(self):
        featured_items = 0
        target_page_name = ""

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))

        while True:
            try:
                self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]' % (featured_items + 1))
                featured_items = featured_items + 1
            except NoSuchElementException:
                break

        for x in range (1, featured_items + 1):
            target_page_name = self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x).get_attribute("text")
            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x))
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x).click()

            target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h1'))).text
            time.sleep(2)
            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="tab-description"]//p[last()]'))
            time.sleep(2)
            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//img'))
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//div[@id="content"]//img').click()
            time.sleep(2)
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))
            time.sleep(2)



    def test_navigation_footer(self):
        footer_items = 0
        target_page_name = ""

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//footer//a')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//footer//a')))

        while True:
            try:
                self.driver.find_element(By.XPATH, '//footer//div[contains (@class, "col")][%d]' % (footer_items + 1))
                footer_items = footer_items + 1
            except NoSuchElementException:
                break

        for x in range (1, footer_items + 1):
            footer_subitem = 1
            while True:
                try:
                    target_page_name = self.driver.find_element(By.XPATH, '//footer//div[contains (@class, "col")][%d]//li[%d]/a' % (x, footer_subitem)).get_attribute("text")
                    if target_page_name in ["Affiliate", "My Account", "Order History", "Wish List", "Newsletter"]:
                        footer_subitem = footer_subitem + 1
                        continue
                    self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//footer//div[contains (@class, "col")][%d]//li[%d]/a' % (x, footer_subitem)))
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, '//footer//div[contains (@class, "col")][%d]//li[%d]/a' % (x, footer_subitem)).click()
                    target_page_name.removesuffix('s')
                    target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//*'))).text
                    time.sleep(1)
                    footer_subitem = footer_subitem + 1
                except NoSuchElementException:
                    break



    def test_product_details(self):
        featured_items = 0
        product_description = ""
        product_tabs = 0

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))

        while True:
            try:
                self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]' % (featured_items + 1))
                featured_items = featured_items + 1
            except NoSuchElementException:
                break

        for x in range (1, featured_items + 1):
            target_page_name = self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x).get_attribute("text")
            product_description = self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//p' % x).text
            product_description.removesuffix('..')

            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x))
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x).click()

            target_page_name in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h1'))).text
            time.sleep(1)
            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//ul[contains (@class, "tabs")]'))
            time.sleep(1)
            while True:
                try:
                    assert product_description in self.driver.find_element(By.XPATH, '//div[@class="tab-description"]//p[%d]' % x).text
                    break
                except AssertionError:
                    continue
                except NoSuchElementException:
                    AssertionError
                    break

            product_tabs = 0
            while True:
                try:
                    self.driver.find_element(By.XPATH, '//div[@id="content"]//ul[contains (@class, "tabs")]/li[%d]' % (product_tabs + 1))
                    product_tabs = product_tabs + 1
                except NoSuchElementException:
                    break

            for x in range(1, product_tabs + 1):
                self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//ul[contains (@class, "tabs")]/li[%d]' % x))
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//div[@id="content"]//ul[contains (@class, "tabs")]/li[%d]' % x).click()
                time.sleep(1)
                WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//div[contains (@id, "tab")][%d][contains (@class, "active")]' % x)))
                time.sleep(1)

            self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//img'))
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//div[@id="content"]//img').click()
            time.sleep(2)
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))
            time.sleep(5)



    def test_search(self):
        target_page_name = ""

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="search"]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="search"]')))

        target_page_name = self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"]//div[@class="content"]//h4/a').get_attribute("text")
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="search"]//button'))
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//div[@id="search"]//button').click()
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="search"]')))
        "Search" in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h1'))).text

        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="search"]//input'))
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//div[@id="search"]//input').send_keys(target_page_name)
        self.driver.find_element(By.XPATH, '//div[@id="search"]//button').click()
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="search"]')))
        "Search" in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h1'))).text



    def test_account_new(self):
        user_first_name = Test_fibernetSite.user_first_name
        user_last_name = Test_fibernetSite.user_last_name
        user_mail = Test_fibernetSite.user_mail
        user_password = Test_fibernetSite.user_password

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]')))

        self.driver.find_element(By.XPATH, '//div[@class="nav float-end"]//span[contains (text(), "Account")]').click()
        time.sleep(3)
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]//div[@class="dropdown"]//ul//a[contains (text(), "Register")]'))).click()
        "Register" in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h1'))).text
        time.sleep(2)

        self.driver.find_element(By.XPATH,'//input[@name="firstname"]').send_keys(user_first_name)
        self.driver.find_element(By.XPATH, '//input[@name="lastname"]').send_keys(user_last_name)
        self.driver.find_element(By.XPATH, '//input[@name="email"]').send_keys(user_mail)
        self.driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(user_password)

        self.driver.find_element(By.XPATH, '//input[@id="input-newsletter-yes"]').click()
        self.driver.find_element(By.XPATH, '//label[@class="form-check-label"]/a/b').click()
        "Registry Policy" in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="modal-information"]//h4'))).text
        self.driver.find_element(By.XPATH, '//div[@id="modal-information"]//button').click()
        WebDriverWait(self.driver, 5).until(ec.invisibility_of_element_located((By.XPATH, '//div[contains (@class, "modal-backdrop")]')))
        self.driver.find_element(By.XPATH, '//input[@name="agree"]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(3)

#        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]//span[contains (text(), "Account")]'))).click()
#        time.sleep(3)
#        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]//div[@class="dropdown"]//ul//a[contains (text(), "Login")]'))).click()
#        time.sleep(2)
#        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="account-login"]')))
#        self.driver.find_element(By.XPATH, '//form[@id="form-login"]//a[contains (text(), "Forgotten Password")]').click()
#        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="account-forgotten"]')))
#        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//input[@name="email"]'))).click()
#        self.driver.find_element(By.XPATH, '//input[@name="email"]').send_keys(user_mail)
#        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
#        time.sleep(1)
#        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="alert"]')))
#        "not found" not in self.driver.find_element(By.XPATH, '//div[@id="alert"]/div').get_attribute("text")
#        time.sleep(1)



    def test_account_login(self):
        user_first_name = Test_fibernetSite.user_first_name
        user_last_name = Test_fibernetSite.user_last_name
        user_mail = Test_fibernetSite.user_mail
        user_password = Test_fibernetSite.user_password

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]')))

        self.driver.find_element(By.XPATH, '//div[@class="nav float-end"]//span[contains (text(), "Account")]').click()
        time.sleep(1)
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]//ul[contains (@class, "dropdown")]//a[contains (text(), "Login")]'))).click()
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="account-login"]')))

        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//input[@name="email"]'))).click()
        self.driver.find_element(By.XPATH, '//input[@name="email"]').send_keys(user_mail)
        self.driver.find_element(By.XPATH, '//input[@name="password"]').send_keys(user_password)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(1)
        assert user_first_name in WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]//div[@class="dropdown"]/a//span'))).text
        assert user_last_name in WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="nav float-end"]//div[@class="dropdown"]/a//span'))).text



    def test_store_purchase_featured(self):
        featured_items = 0
        purchased_items = 0
        target_item_name = ""

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="common-home"]//div[@class="col"]//div[@class="product-thumb"]')))
        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="header-cart"]//button[contains (text(), "0 item")]')))

        while True:
            try:
                self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]' % (featured_items + 1))
                featured_items = featured_items + 1
            except NoSuchElementException:
                break

        for x in range(1, featured_items + 1):
            target_item_name = self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x).get_attribute("text")
            if x % 2 == 1:
                self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//button[contains (@aria-label, "Cart")]' % x))
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//button[contains (@aria-label, "Cart")]' % x).click()
                WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="alert"]/div[contains (text(), "added")]')))
                target_item_name in WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="alert"]/div/a'))).get_attribute("text")
                self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="header-cart"]//button'))
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="header-cart"]//button//i[contains (text(), "%d item")]' % (purchased_items + x))))

            elif x % 2 == 0:
                self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x))
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//div[@id="content"]//div[@class="col"][%d]//div[@class="content"]//a' % x).click()
                WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="product"]//input[@name="quantity"]')))
                WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="product"]//button[contains (text(), "Add")]')))
                time.sleep(3)

                self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="product"]//label[contains (@for, "quantity")]'))
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//div[@id="product"]//input[@name="quantity"]').click()
                self.driver.find_element(By.XPATH, '//div[@id="product"]//input[@name="quantity"]').clear()
                self.driver.find_element(By.XPATH, '//div[@id="product"]//input[@name="quantity"]').send_keys(x)
                self.driver.find_element(By.XPATH, '//div[@id="product"]//label').click()
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//div[@id="product"]//button[@type="submit"][@id="button-cart"]').click()
                WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="alert"]/div[contains (text(), "added")]')))
                target_item_name in WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="alert"]/div/a'))).get_attribute("text")
                self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, '//div[@id="header-cart"]//button'))
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="header-cart"]//button//i[contains (text(), "%d item")]' % (purchased_items + x))))

            purchased_items = purchased_items + x

        try:
            self.driver.find_element(By.XPATH, '//div[@id="alert"]//button').click()
        finally:
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//div[@class="nav float-end"]//a[title="Shopping Cart"]').click()
        "Shopping Cart" in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="content"]//h1'))).text
        WebDriverWait(self.driver, 5).until(ec.invisibility_of_element_located((By.XPATH, '//div[@id="content"]//p')))
















    def est_navigation_instore(self):
        store_categories = 0
        store_type = ""
        store_subcategories = 0
        target_page_name = ""

        self.driver = Test_fibernetSite.driver
#        self.driver.get(Test_fibernetSite.site_address)



        while True:
            try:
                self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % (store_categories + 1))))
                store_categories = store_categories + 1
            except NoSuchElementException:
                break

        for x in range (1, store_categories + 1):
            store_subcategories = 0
            store_type = ""
            store_type = self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x))).get_attribute("class")
            if store_type == "nav-item dropdown":
                self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x))).click()
                while True:
                    try:
                        self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]//li[%d]/a' % (x, store_subcategories + 1))))
                        store_subcategories = store_subcategories + 1
                    except NoSuchElementException:
                        break

                for y in range (1, store_subcategories + 1):
                    self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x))).click()
                    target_page_name = ((self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]//li[%d]/a' % (x, y)))).get_attribute("text")).split(" ("))[0]
                    self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]//li[%d]' % (x, y)))).click()
                    target_page_name in WebDriverWait(self.driver, 15).until(ec.text_to_be_present_in_element((By.XPATH, '//div[@id="content"]//h2'), target_page_name)).text
                    target_page_name in WebDriverWait(self.driver, 15).until(ec.text_to_be_present_in_element((By.XPATH, '//aside[@id="column-left"]//a[contains (@class, "active")]'), target_page_name)).text

                self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x))).click()
                target_page_name = self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]/a' % x))).get_attribute("text")
                self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]/div/a' % x))).click()
                target_page_name in WebDriverWait(self.driver, 15).until(ec.text_to_be_present_in_element((By.XPATH, '//div[@id="content"]//h2'), target_page_name)).text
                target_page_name in WebDriverWait(self.driver, 15).until(ec.text_to_be_present_in_element((By.XPATH, '//aside[@id="column-left"]//a[contains (@class, "active")]'), target_page_name)).text

            elif store_type == "nav-item":
                target_page_name = self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x))).get_attribute("text")
                self.driver.find_element(By.XPATH(('//nav[@id="menu"]//li[contains (@class, "nav-item")][%d]' % x))).click()
                target_page_name in WebDriverWait(self.driver, 15).until(ec.text_to_be_present_in_element((By.XPATH, '//div[@id="content"]//h2'), target_page_name)).text
                target_page_name in WebDriverWait(self.driver, 15).until(ec.text_to_be_present_in_element((By.XPATH, '//aside[@id="column-left"]//a[contains (@class, "active")]'), target_page_name)).text

            Test_fibernetSite.store_subcategories_in.append(store_subcategories)
        Test_fibernetSite.store_categories_in = store_categories










    def test_review_view(self):
        pass




    def test_review_submit(self):
        pass






    def test_search_xss(self):
        xss_search_text = "<script>alert('XSS attack attempt')</script>"

        self.driver = Test_fibernetSite.driver
        try:
            WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="search"]')))
        except TimeoutException:
            self.driver.get(Test_fibernetSite.site_address)
            WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="search"]')))

        self.driver.find_element(By.XPATH, '//div[@id="search"]//input').send_keys(xss_search_text)
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//div[@id="search"]//button').click()
        WebDriverWait(self.driver, 15).until(ec.invisibility_of_element_located((By.XPATH, '//div[@id="search"]')))
        time.sleep(5)



    def test_multi_copy_ddos(self):
        pass



    def test_interact_speed_lock(self):
        self.driver = Test_fibernetSite.driver

        for x in range (1, 101):
            self.driver.get(Test_fibernetSite.site_address)
            try:
                WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//div[@id="content"]')))
            except TimeoutException:
                break

        WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//div[@id="challenge-stage"]')))
        "Verifying you are human" in WebDriverWait(self.driver, 15).until(ec.visibility_of_element_located((By.XPATH, '//h2[contains (@id, "challenge")]'))).text



    def test_cleanup(self):
        Test_fibernetSite.driver.quit()
