import pandas as pd
import os
from time import sleep
from typing import Type
from datetime import datetime, timedelta
from contextlib import suppress
import json
from tqdm import tqdm
from clear import clear
from bot.varas_dict import varas
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import *
import threading


class ExtractPauta:
    
    def __init__(self) -> None:
        pass

        self.varas = varas()
        
    def execution(self):
        
        self.appends = {}
        clear()
        
        threads = []
        
        pos = 5
        
        for vara in tqdm(list(self.varas), position=-1):
            if len(threads) == 4:
                sleep(60)
                threads.clear()
            
            options = Options()
            options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
            path = os.path.join(os.getcwd(), "geckodriver.exe")
            driver = webdriver.Firefox(service=Service(path), options=options)
            wait = WebDriverWait(driver, 10)
            starter = threading.Thread(target=self.queue, args=(vara, driver, wait, pos, ))
            threads.append(starter.name)
            starter.start()
            pos += 1
            sleep(30)
            
        
        filename = "varas.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.appends, f, ensure_ascii=False, indent=4)
    
    def queue(self, vara: str, driver: Type[WebDriver], wait: Type[WebDriverWait], pos: int):
        
        self.wait = wait
        self.driver = driver
        
        if not self.appends.get(vara, None):
            self.appends[vara] = {}
            
        judge = str(self.varas.get(vara))

        start_date = datetime.strptime('2024-07-12', '%Y-%m-%d')
        end_date = datetime.strptime('2024-12-31', '%Y-%m-%d')
        total_days = end_date - start_date
        bar = tqdm(range(1, total_days.days), position=pos)
        # Use um loop para adicionar cada data ao intervalo
        current_date = start_date
        while current_date <= end_date:
            
            date = current_date.strftime('%Y-%m-%d')
            self.data_append = self.appends[vara][date] = []
            driver.get(f"https://pje.trt11.jus.br/consultaprocessual/pautas{judge}-{date}")
            self.get_pautas()
            current_date += timedelta(days=1)
            
            if len(self.appends[vara][date]) == 0:
                self.appends[vara].pop(date)
                
            bar.update()
                
        filename = f"{vara}.json"
        
        if not len(self.appends[vara]) == 0:
        
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.appends[vara], f, ensure_ascii=False, indent=4)
            
        driver.quit()
             
    def get_pautas(self):
        
        sleep(3)
        try:
            table_pautas: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table[name="Tabela de itens de pauta"]')))
            itens_pautas = None
            
            with suppress(NoSuchElementException, TimeoutException):
                itens_pautas = table_pautas.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            
            if itens_pautas:
                for item in itens_pautas:
                    
                    
                    item: WebElement = item
                    itens_tr = item.find_elements(By.TAG_NAME, 'td')
                    
                    appends = {"indice": itens_tr[0].text,
                            "Horário": itens_tr[1].text,
                            "Tipo": itens_tr[2].text,
                            "Processo": itens_tr[3].find_element(By.TAG_NAME, 'a').text,
                            "Partes": itens_tr[3].find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').text,
                            "Sala": itens_tr[5].text,
                            "Situação": itens_tr[6].text}
                    
                    self.data_append.append(appends)
                    
                    pass
            
                btn_next = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Próxima página"]')
                
                buttondisabled = btn_next.get_attribute("disabled")
                if not buttondisabled:
                    
                    btn_next.click()
                    self.get_pautas()
                    
        except Exception as e:
            print(e)
            pass
        
    
                


