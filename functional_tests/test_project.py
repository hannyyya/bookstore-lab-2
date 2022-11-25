from selenium import webdriver
from Bookstore.Website.models import User
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
from selenium.webdriver.common.by import By

link = "http://127.0.0.1:8000/"
browser = webdriver.Firefox()
browser.get(link)
