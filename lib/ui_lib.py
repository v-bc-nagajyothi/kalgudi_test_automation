"""
Various helper methods and WebDriver wrappers
specifically targetting the Bigcommerce Control Panel.
"""

from includes import *
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class CommonMethods():
    def __init__(self, browser):
        """
        A constructor
        :param browser: an existing webdriver browser object
        :raise AttributeError: if browser is not a webdriver browser object
        """
        if not type(browser).__name__ == 'WebDriver':
            raise AttributeError("argument is not a valid selenium WebDriver object, got object of type '%s' " %
                                 type(browser).__name__)
        self.browser = browser

    @property
    def browser(self):
        """
        The webdriver browser object currently being used by this class
        :return: webdriver browser object
        """
        return self.browser

    def __getattr__(self, attr):
        """
        Called when an attribute lookup has not found the attribute in the usual places. This method checks if a
        webdriver browser object responds to 'attr' and calls it if it does. Throws an AttributeError if browser does
        not respond to 'attr'
        :param attr:
        :return: :raise AttributeError:
        """

        def make_interceptor(callable_method):
            def func(*args, **kwargs):
                return callable_method(*args, **kwargs)
            return func
        att = None
        if hasattr(self.browser, attr):
            att = getattr(self.browser, attr)
        if callable(att):
            return make_interceptor(att)
        else:
            raise AttributeError("The browser instance has no attribute '%s'" % attr)

    def _find(self, selector, plural=False, selector_type="id"):
        """
        A private convenience method that calls any of find_elements_* method depending on selector_type
        :param selector:
        :param plural:
        :param selector_type:
        :return: :raise TypeError:
        """
        selector_type = selector_type.lower()

        s_methods = {
            "id": "find_element_by_id",
            "css": "find_element_by_css_selector",
            "xpath": "find_element_by_xpath",
            "partial_link": "find_element_by_partial_link_text",
            "link": "find_element_by_link_text",
            "link_text": "find_element_by_link_text",
            "name": "find_element_by_name",
            "class": "find_element_by_class_name",
            "tag": "find_element_by_tag_name"
        }

        p_methods = {
            "id": "find_elements_by_id",
            "css": "find_elements_by_css_selector",
            "xpath": "find_elements_by_xpath",
            "partial_link": "find_elements_by_partial_link_text",
            "link": "find_elements_by_link_text",
            "link_text": "find_elements_by_link_text",
            "name": "find_elements_by_name",
            "class": "find_elements_by_class_name",
            "tag": "find_elements_by_tag_name"
        }

        try:
            method_name = s_methods[selector_type]
            if plural:
                method_name = p_methods[selector_type]

            attr = getattr(self.browser, method_name)(selector)
            return attr
        except KeyError:
            raise TypeError("Invalid selector type")

    def find(self, selector, iterator=0, plural=False):
        """
        A convenience method to find an element that matches a selector without having to specify a selector
        :param selector: can be an id, css, xpath, name, class, link text or partial link text
        :param iterator: for internal use don't use this argument
        :param plural: for internal use don;t use this argument
        :return: a webdriver element
        :raise webdriver.NoSuchElementException:
        """
        types = ["class", "css", "xpath", "id", "link_text", "name", "link", "partial_link", "tag"]

        if iterator >= len(types):
            raise NoSuchElementException()

        try:
            element = self._find(selector, plural, types[iterator])
            if type(element).__name__ == 'list' and len(element) == 0:
                raise NoSuchElementException()
            return element
        except:
            return self.find(selector, iterator + 1, plural)

    def find_all(self, selector):
        """
        A convenience method to find all elements that match a selector without having to specify a selector_type.
        :param selector: can be an id, css, xpath, name, class, link text or partial link text
        :return: list of elements that match selector
        """
        return self.find(selector, iterator=0, plural=True)

    def login(self, browser, username, password):
        browser.find_element_by_id('user_email').clear()
        browser.find_element_by_id('user_email').send_keys(username)
        browser.find_element_by_id('user_password').send_keys(password)
        browser.find_element_by_xpath('//input[@value="Log in"]').click()

    def go_to_admin(self, browser, url, username, password, check_for_login=False):
        """
        Navigate to control panel login page
        Enter valid login credentials & login
        """
        admin = urlparse.urljoin(url, 'admin')
        browser.get(admin)

        try:
            self.login(browser, username, password)
            self.check_for_slick()
        except NoSuchElementException:
            if check_for_login:
                raise Exception('login window not found')

            try:
                admin = urlparse.urljoin(url, 'admin/login')
                browser.get(admin)
                self.login_without_ana(browser, url, username, password)
            except:
                admin = urlparse.urljoin(url, 'admin')
                browser.get(admin)


    @staticmethod
    def generate_random_string(size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def wait_until_element_present(self, element, searchby, browser=None, time = 30, first = True):
        try:
            if not browser:
                browser=self.browser
            if searchby == "ID":
                WebDriverWait(browser, time).until(lambda s: self.find_element_by_id(element).is_displayed() and self.find_element_by_id(element))
                return self.find_element_by_id(element)
            elif searchby == "XPATH":
                WebDriverWait(browser, time).until(lambda s: self.find_element_by_xpath(element).is_displayed() and self.find_element_by_xpath(element))
                return self.find_element_by_xpath(element)
            elif searchby == "NAME":
                WebDriverWait(browser, time).until(lambda s: self.find_element_by_name(element).is_displayed() and self.find_element_by_name(element))
                return self.find_element_by_name(element)
            elif searchby == "LINK":
                WebDriverWait(browser, time).until(lambda s: self.find_element_by_link_text(element).is_displayed() and self.find_element_by_link_text(element))
                return self.find_element_by_link_text(element)
            elif searchby == "CSS_SELECTOR":
                WebDriverWait(browser, time).until(lambda s: self.find_element_by_css_selector(element).is_displayed() and self.find_element_by_css_selector(element))
                return self.find_element_by_css_selector(element)
            elif searchby == "CLASS_NAME":
                WebDriverWait(browser, time).until(lambda s: self.find_element_by_class_name(element).is_displayed() and self.find_element_by_class_name(element))
                return self.find_element_by_class_name(element)
            elif searchby == "TAGNAME":
                WebDriverWait(browser, time).until(lambda s: self.find_element_by_tag_name(element).is_displayed() and self.find_element_by_tag_name(element))
                return browser.find_element_by_tag_name(element)
            elif searchby == "JQUERY":
                WebDriverWait(browser, time).until(lambda s: self.execute_script(element))
        except TimeoutException:
            browser.save_screenshot('timeout.png')
            raise
        except StaleElementReferenceException:
            if first:
                return self.wait_until_element_present(browser, element, searchby, time, False)
            else:
                browser.save_screenshot('stale_element.png')
                raise

    def select_dropdown_value(self, browser, dropdown_id, option_text):
        dropdown_list = self.wait_until_element_present(dropdown_id, 'ID')
        for option in dropdown_list.find_elements_by_tag_name('option'):
            if option.text == option_text:
                option.click()

    def get_dropdown_selected_value(self, browser, element_id):
        return browser.execute_script("return $('#" + element_id + " option:selected').text()")

    def clear_field(self, browser, element_id):
        WebDriverWait(browser, 30).until(lambda s: s.find_element_by_id(element_id).is_displayed() and s.find_element_by_id(element_id))
        browser.find_element_by_id(element_id).clear()

    def verify_and_assert_success_message(self, browser, success_message, classname):
        # StaleElementReferenceException: Message: u'Element is no longer attached to the DOM' ; Stacktrace: Method fxdriver.cache.getElementAt threw an error in resource://fxdriver/modules/web_element_cache.js
        try:
            WebDriverWait(browser, 40).until(lambda s: success_message in s.find_element_by_css_selector(classname).text)
            assert success_message in browser.find_element_by_css_selector(classname).text
        except StaleElementReferenceException:
            WebDriverWait(browser, 40).until(lambda s: success_message in s.find_element_by_css_selector(classname).text)
            assert success_message in browser.find_element_by_css_selector(classname).text

    def select_dropdown_value_by_css(self, browser, dropdown_class, option_text):
        WebDriverWait(browser, 30).until(lambda s: s.find_element_by_css_selector(dropdown_class).is_displayed() and s.find_element_by_css_selector(dropdown_class))
        dropdown_list = browser.find_element_by_css_selector(dropdown_class)
        for option in dropdown_list.find_elements_by_tag_name('option'):
            if option.text == option_text:
                option.click()

    def get_dropdown_values(self, browser, dropdown_id):
        WebDriverWait(browser, 30).until(lambda s: s.find_element_by_id(dropdown_id).is_displayed() and s.find_element_by_id(dropdown_id))
        dropdown_list = browser.find_element_by_id(dropdown_id)
        option_text = ""
        for option in dropdown_list.find_elements_by_tag_name('option'):
            option_text = option_text + option.text + ' '

        return option_text

    def element_exists(self, selector, browser=None, search_by="ID"):
        try:
            self.wait_until_element_present(selector, search_by, browser)
            return True
        except (NoSuchElementException, Exception):
            return False

    def enter_text(self, selector, value, browser=None, search_by="ID"):
        element = self.find_element_by_id(selector)
        element.clear()
        element.send_keys(value)
