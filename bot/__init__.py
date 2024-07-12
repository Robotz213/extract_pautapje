from time import sleep
from typing import Type
from contextlib import suppress


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

varas = {
    "1ª Vara do Trabalho de Boa Vista": "#VTBV1-1",
    "2ª Vara do Trabalho de Boa Vista": "#VTBV2-1",
    "3ª Vara do Trabalho de Boa Vista": "#VTBV3-1",
    "51ª Vara Digital do Núcleo de Justiça 4.0 - RR": "#51VDRR-1",
    "52ª Vara Digital do Núcleo de Justiça 4.0 - RR": "#52VDRR-1",
    "53ª Vara Digital do Núcleo de Justiça 4.0 - RR": "#53VDRR-1",
    "CEJUSC - BOA VISTA": "#CBV-1",
    "1ª Vara do Trabalho de Coari": "#1VTC-1",
    "1ª Vara do Trabalho de Eirunepé": "#VTE-1",
    "1ª Vara do Trabalho de Humaitá": "#1VTH-1",
    "1ª Vara do Trabalho de Itacoatiara": "#VTI-1",
    "1ª Vara do Trabalho de Lábrea": "#1VTL-1",
    "1ª Vara do Trabalho de Manacapuru": "#1VTM-1",
    "1ª Vara do Trabalho de Manaus": "#VT1",
    "2ª Vara do Trabalho de Manaus": "#VT2",
    "3ª Vara do Trabalho de Manaus": "#VT3",
    "4ª Vara do Trabalho de Manaus": "#VT4",
    "5ª Vara do Trabalho de Manaus": "#VT5",
    "6ª Vara do Trabalho de Manaus": "#VT6",
    "7ª Vara do Trabalho de Manaus": "#VT7",
    "8ª Vara do Trabalho de Manaus": "#VT8",
    "9ª Vara do Trabalho de Manaus": "#VT9",
    "10ª Vara do Trabalho de Manaus": "#VTL-10",
    "11ª Vara do Trabalho de Manaus": "#VTL-11",
    "12ª Vara do Trabalho de Manaus": "#VTL-12",
    "13ª Vara do Trabalho de Manaus": "#VTL-13",
    "14ª Vara do Trabalho de Manaus": "#VTL-14",
    "15ª Vara do Trabalho de Manaus": "#VTL-15",
    "16ª Vara do Trabalho de Manaus": "#VTL-16",
    "17ª Vara do Trabalho de Manaus": "#VTL-17",
    "18ª Vara do Trabalho de Manaus": "#VTL-18",
    "19ª Vara do Trabalho de Manaus": "#VTL-19",
    "1ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "2ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "3ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "4ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "5ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "6ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "7ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "8ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "9ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "10ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "11ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "12ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "13ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "14ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "15ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "16ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "17ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "18ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "19ª Vara Digital do Núcleo de Justiça 4.0 - AM": "",
    "Secretaria de Execução da Fazenda Pública": "",
    "SEÇÃO DE HASTAS PÚBLICAS- SEHASP": "",
    "CEJUSC-JT 1º grau": "",
    "Divisão de Execução Concentrada": "",
    "Divisão de Pesquisa Patrimonial": "",
    "Projeto Garimpo - 1º Grau": "",
    "Corregedoria-Geral;": "",
    "1ª Vara do Trabalho de Parintins": "",
    "1ª Vara do Trabalho de Presidente Figueiredo": "",
    "1ª Vara do Trabalho de Tabatinga": "",
    "1ª Vara do Trabalho de Tefé": ""
}


class ExtractPauta:
    
    def __init__(self) -> None:
        pass

        path = GeckoDriverManager().install()
        self.driver = webdriver.Firefox(service=Service(path))
        self.wait = WebDriverWait(self.driver, 10)
        
        
    def execution(self):
        
        self.driver.get("https://pje.trt11.jus.br/consultaprocessual/pautas")
        
        get_orgaojudge = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="cdk-overlay-container"]')))
        get_orgaojudge.click()
        
        sleep(1)
        
        
        
        pass


