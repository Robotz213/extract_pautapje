import pandas as pd
import os
from time import sleep
from typing import Type
from datetime import datetime, timedelta
from contextlib import suppress
import json
import random
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium import *
import threading

def gerar_cor_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class ExtractPauta:
    
    def __init__(self) -> None:
        pass

        self.varas = varas()
        
    def execution(self):
        
        self.appends = {}
        clear()
        
        threads = []
        
        pos = 5
        count = 0
        for vara in tqdm(list(self.varas), position=-1, colour=gerar_cor_hex()):
            
            count = 0
            while len(threads) >= 4:
                
                count +=1
                free_thread = None
                for thread in threads:
                    thread: threading.Thread = thread
                    if not thread.is_alive():
                        free_thread = thread
                        break
                    
                if free_thread:
                    threads.remove(free_thread)
                    break
                 
                if count == 4:       
                    filename = "varas.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.appends, f, ensure_ascii=False, indent=4)
                        
            options = Options()
            options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
            path = os.path.join(os.getcwd(), "geckodriver.exe")
            driver = webdriver.Firefox(service=Service(path), options=options)
            wait = WebDriverWait(driver, 10)
            starter = threading.Thread(target=self.queue, args=(vara, driver, wait, pos, ))
            threads.append(starter)
            starter.start()
            pos += 2
            sleep(30)
        
        filename = "varas.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.appends, f, ensure_ascii=False, indent=4)
    
    def queue(self, vara: str, driver: Type[WebDriver], wait: Type[WebDriverWait], pos: int):
        
        if not self.appends.get(vara, None):
            self.appends[vara] = {}
            
        judge = str(self.varas.get(vara))
        filename = f"{vara}.json"
        start_date = datetime.strptime('2024-07-12', '%Y-%m-%d')
        end_date = datetime.strptime('2024-12-31', '%Y-%m-%d')
        total_days = end_date - start_date
        bar = tqdm(range(1, total_days.days), position=pos, colour=gerar_cor_hex())
        
        current_date = start_date
        while current_date <= end_date:
            
            date = current_date.strftime('%Y-%m-%d')
            self.data_append = self.appends[vara][date] = []
            driver.get(f"https://pje.trt11.jus.br/consultaprocessual/pautas{judge}-{date}")
            self.get_pautas(driver, wait)
            current_date += timedelta(days=1)
            
            if len(self.appends[vara][date]) == 0:
                self.appends[vara].pop(date)
            
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.appends[vara], f, ensure_ascii=False, indent=4)
            bar.update()
                
        
        
        if not len(self.appends[vara]) == 0:
        
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.appends[vara], f, ensure_ascii=False, indent=4)
            
        driver.quit()
             
    def get_pautas(self, driver: Type[WebDriver], wait: Type[WebDriverWait]):
        
        try:
            
            times = 4
            
            table_pautas: WebElement = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'pje-data-table[id="tabelaResultado"]')))
            table_pautas: WebElement = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[name="Tabela de itens de pauta"]')))
            itens_pautas = None
            
            with suppress(NoSuchElementException, TimeoutException):
                itens_pautas = table_pautas.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
            
            if itens_pautas:
                times = 6
                for item in itens_pautas:
                    
                    with suppress(StaleElementReferenceException):
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

                try:
                    btn_next = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Próxima página"]')
                    
                    buttondisabled = btn_next.get_attribute("disabled")
                    if not buttondisabled:
                        
                        btn_next.click()
                        self.get_pautas(driver, wait)

                except Exception as e:
                    tqdm.write(f"{e}")
            
            sleep(times)
                 
        except Exception as e:
            tqdm.write(f"{e}")
            pass
        
    
                


