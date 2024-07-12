import pandas as pd
from time import sleep
from typing import Type
from datetime import datetime, timedelta
from contextlib import suppress
import json
from tqdm import tqdm

from bot.varas_dict import varas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException



class ExtractPauta:
    
    def __init__(self) -> None:
        pass

        self.varas = varas()
        
        path = GeckoDriverManager().install()
        self.driver = webdriver.Firefox(service=Service(path))
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()
        
    def execution(self):
        
        self.appends = {}
        for vara in tqdm(list(self.varas)):
            
            if not self.appends.get(vara, None):
                self.appends[vara] = {}
            
            judge = str(self.varas.get(vara))

            start_date = datetime.strptime('2024-07-12', '%Y-%m-%d')
            end_date = datetime.strptime('2024-07-30', '%Y-%m-%d')

            # Use um loop para adicionar cada data ao intervalo
            current_date = start_date
            while current_date <= end_date:
                
                date = current_date.strftime('%Y-%m-%d')
                self.data_append = self.appends[vara][date] = []
                self.driver.get(f"https://pje.trt11.jus.br/consultaprocessual/pautas{judge}-{date}")
                self.get_pautas()
                current_date += timedelta(days=1)
            filename = f"{vara}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.appends, f, ensure_ascii=False, indent=4)
                
            
        
        filename = "varas.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.appends, f, ensure_ascii=False, indent=4)
                
    def get_pautas(self):
        
        sleep(3)
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
        
    
                


