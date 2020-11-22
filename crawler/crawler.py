# Crawler based on https://github.com/vinirusso/telegram-bot-agenda-presidencial

from crawler.webdriver_wrapper import WebDriverWrapper
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import os
from datetime import date, datetime, timedelta
import pandas as pd 
import yaml

class PresidentialAgendaCrawler:
    def __init__(self, csv_path, base_url):
        self.base_url = base_url
        self.driver = WebDriverWrapper()._driver
        self.wait = WebDriverWait(self.driver, 10)
        self.csv_path = csv_path 

    def scrape_datarange(self, begin, end):
        #Defina os dias de inicios e fim
        delta = end - begin
        for i in range(delta.days):
            current = begin + timedelta(days=i)
            print("Current Data", current)
            self.scrape(current)

    def scrape(self, day):
        items_agenda = []
        day_string = day.strftime("%Y-%m-%d")
        print('Dia: '+ day_string)
        self.driver.get(self.base_url + day_string)
        time.sleep(5)
        compromissos = self.driver.find_elements_by_class_name("item-compromisso")
        try:
            for compromisso in compromissos:
                horario = '*Horário:* '+ compromisso.find_element_by_xpath(".//time").text + '\n'
                titulo = compromisso.find_element_by_xpath(".//h4[@class='compromisso-titulo']").text + '\n'
                local = '*Local:* ' + compromisso.find_element_by_xpath(".//p[@class='compromisso-local']").text + '\n'
                items_agenda.append([day_string, horario, titulo, local])
        except:
            print('Not Found')

        df = pd.DataFrame(items_agenda)
        df.to_csv(self.csv_path, encoding = "ISO-8859-1", mode = 'a', header = False)