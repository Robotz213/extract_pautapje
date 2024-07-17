import pandas as pd


import os
import json

import platform
import threading
import subprocess
from tqdm import tqdm
from time import sleep
from clear import clear
from typing import Type
from datetime import datetime
from datetime import timedelta
from contextlib import suppress


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from termcolor import colored
from bot.varas_dict import varas
from bot.misc.hex_color import gerar_cor_hex


class ExtractPauta:

    def __init__(self, vara: str, date_inicio: Type[datetime], date_fim: Type[datetime]) -> None:
        
        clear()
        os.makedirs("json", exist_ok=True)
        
        self.vara = vara
        
        self.date_inicio = date_inicio
        self.date_fim = date_fim
        
        self.appends = {}
        self.threads = []
        self.firefox_bin = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        self.options = Options()
        self.options.binary_location = self.firefox_bin
        self.path = os.path.join(os.getcwd(), "geckodriver.exe")
        self.pos = 0
        self.sys = {"Linux": "bin",
                    "Windows": "Scripts"}
        
        self.varas = varas()
        
    def execution(self):

        ## Intera sobre as varas do dicionario, assim permite buscar por data
        ## em todos os juizados sem depender que ele espere finalizar uma vara
        ## para inicializar outra

        # Delimita a quantidade de threads para evitar sobrecarga de memória
        while len(self.threads) > 0:

            free_thread = None
            for thread in self.threads:
                thread: threading.Thread = thread
                
                
                if not thread.is_alive():
                    free_thread = thread
                    break

            if free_thread:
                
                ## Esse arquivo .json salva todas as buscas em um único arquivo
                filename = os.path.join(os.getcwd(), "json", "pautas.json")
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.appends, f, ensure_ascii=False, indent=4)

                argumentos = [filename]
                sistema = platform.system()

                python_path = f".venv/{self.sys.get(sistema)}/python"
                subprocess.run([python_path, "makexlsx.py"] + argumentos)
                return
        
        # Inicializador do WebDriver
        driver = webdriver.Firefox(
            service=Service(self.path), options=self.options)
        
        # Maximiza a window para evitar erros de interação com elementos
        driver.maximize_window()

        wait = WebDriverWait(driver, 10)
        
        # Inicia a execução em uma Thread
        starter = threading.Thread(
            target=self.queue, args=(self.vara, driver, wait,))
        self.threads.append(starter)
        starter.start()
        self.execution()

    def queue(self, vara: str, driver: Type[WebDriver], wait: Type[WebDriverWait]):

        if not self.appends.get(vara, None):
            self.appends[vara] = {}

        judge = str(self.varas.get(vara))
        filename = os.path.join(os.getcwd(), "json", f"{vara}.json")

        self.current_date = current_date = self.date_inicio
        while self.date_fim >= current_date:

            date = current_date.strftime('%Y-%m-%d')
            self.data_append = self.appends[vara][date] = []
            
            ## O filtro funciona conforme a URL. Veja o "varas_dict.py"
            ## Defini conforme o TRT 11, atualize esse arquivo conforme seu estado
            ## No TRT11, é "url/pautas{juizado}-{data_filtro}"
            
            ## Exemplo: https://pje.trt11.jus.br/consultaprocessual/pautas#VTBV3-1-2024-07-24
            
            driver.get(
                f"https://pje.trt11.jus.br/consultaprocessual/pautas{judge}-{date}")
            self.get_pautas(driver, wait)
            current_date += timedelta(days=1)

            if len(self.appends[vara][date]) == 0:
                self.appends[vara].pop(date)

            # Eu optei por salvar em ".json", mas caso queria outro formato, aconselho criar um arquivo apêndice
            # Parecido com o que eu fiz em "makexlsx.py", onde ele chama o Pandas e converte o json gerado em xlsx
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.appends[vara], f, ensure_ascii=False, indent=4)
        
        if not len(self.appends[vara]) == 0:

            ## Salva a extração por vara caso queira algo mais específico
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.appends[vara], f, ensure_ascii=False, indent=4)

        driver.quit()

    def get_pautas(self, driver: Type[WebDriver], wait: Type[WebDriverWait]):

        try:
            
            clear()
            
            tqdm.write(colored(f"Buscando pautas na data {self.current_date.strftime("%d/%m/%Y")}", "yellow", attrs=["bold"]))
            ## Interage com a tabela de pautas
            driver.implicitly_wait(2)
            times = 4
            itens_pautas = None
            table_pautas: WebElement = wait.until(EC.all_of(EC.presence_of_element_located((By.CSS_SELECTOR, 'pje-data-table[id="tabelaResultado"]'))),
                                      (EC.visibility_of_element_located((By.CSS_SELECTOR, 'table[name="Tabela de itens de pauta"]'))))[-1]

            
            with suppress(NoSuchElementException, TimeoutException):
                itens_pautas = table_pautas.find_element(
                    By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

            ## Caso encontre a tabela, raspa os dados
            if itens_pautas:
                
                tqdm.write(colored("\n Pautas encontradas!\n", "green", attrs=["bold"]))
                
                times = 6
                
                for item in tqdm(itens_pautas, desc=colored("Extraindo pautas...", "green", attrs=["underline"]), unit="Pauta"):

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
                    btn_next = driver.find_element(
                        By.CSS_SELECTOR, 'button[aria-label="Próxima página"]')

                    buttondisabled = btn_next.get_attribute("disabled")
                    if not buttondisabled:

                        btn_next.click()
                        self.get_pautas(driver, wait)

                except Exception as e:
                    tqdm.write(f"{e}")

            else:
                tqdm.write(colored(f"Nenhuma pauta encontrada", "red", attrs=["bold"]))
            ## Eu defini um timer, um caso encontre a tabela e outro
            ## para caso não encontre ela
            
            sleep(times)

        except Exception as e:
            tqdm.write(f"{e}")
