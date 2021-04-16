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
import random 
from pathlib import Path

class PresidentialAgendaCrawler:
    def __init__(self, csv_path, base_url):
        self.base_url = base_url
        self.driver = WebDriverWrapper()._driver
        self.wait = WebDriverWait(self.driver, 10)
        self.csv_path = Path(csv_path) 

    def scrape_datarange(self, begin, end):
        #Defina os dias de inicios e fim
        delta = end - begin
        compromisso = []
        for i in range(delta.days):
            current = begin + timedelta(days=i)
            print("Extracting Data", current)
            data = self.scrape(current)
            compromisso.extend(data)
            
        if len(compromisso) > 0:
            print("Saving results\n")
            df = pd.DataFrame(compromisso, columns = ['data', 'inicio', 'fim', 'titulo', 'local', 'participantes'])
            if self.csv_path.exists():
                df.to_csv(self.csv_path, encoding = "utf-8", index = False, mode = 'a', header = False)
            else:
                df.to_csv(self.csv_path, encoding = "utf-8", index = False)

    def scrape(self, day):
        items_agenda = []
        day_string = day.strftime("%Y-%m-%d")
        self.driver.get(self.base_url + day_string)
        time.sleep(random.randint(1, 6))
        compromissos = self.driver.find_elements_by_class_name("item-compromisso")
        try:
            for compromisso in compromissos:
                inicio = compromisso.find_element_by_xpath(".//time[@class='compromisso-inicio']").text
                fim = ""
                try:
                    fim = compromisso.find_element_by_xpath(".//time[@class='compromisso-fim']").text
                except:
                    pass

                titulo = ""
                try:
                    titulo = compromisso.find_element_by_xpath(".//h4[@class='compromisso-titulo']").text.replace(",", " - ")
                except:
                    try: 
                        titulo = compromisso.find_element_by_xpath(".//h4[@class='compromisso-titulo toggle closed']").text.replace(",", " - ")
                    except:
                        pass
                
                local = compromisso.find_element_by_xpath(".//div[@class='compromisso-local']").text.replace(",", " - ")
                participantes = ""
                try:
                    pessoas = [x.get_attribute("innerHTML").strip().replace(",", " - ") for x in compromisso.find_element_by_xpath(".//div[@class='compromisso-participantes']").find_elements_by_tag_name('li')]
                    participantes = ';'.join(pessoas)
                except:
                    pass
                items_agenda.append([day_string, inicio, fim, titulo, local, participantes])
        except:
            print('Not Found')

        return items_agenda
        