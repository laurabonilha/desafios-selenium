'''
PROPOSTA DO DESAFIO: A AUTOMAÇÃO DEVERÁ ACESSAR O SITE COIN GECKO (https://www.coingecko.com/pt).
DEPOIS, A AUTOMAÇÃO DEVE ALTERAR A MOEDA PARA REAL.
APÓS ALTERAR A MOEDA, DEVERÁ CAPTURAR TODOS OS DADOS DE CRIPTOMOEDAS.
TODAS AS INFORMAÇÕES DAS CRIPTOMOEDAS DEVEM SER SALVAS EM UM ARQUIVO CSV E TAMBÉM EM UMA PLANILHA EXCEL PARA VISUALIZAÇÃO.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select #seleção de campos web
import re
import pandas as pd
import time
import json

driver = webdriver.Chrome()
# Criando uma variável de espera padrão
wait = WebDriverWait(driver=driver, timeout=15, poll_frequency=1)
driver.get('https://www.coingecko.com/pt')

# Aguardando elemento que indique carregamento total da página
wait.until(EC.presence_of_element_located(locator=(By.XPATH, '/html/body/header/div[2]/div[3]/div/div[1]/a[1]/img[1]')))

# Encontrando o botão de configurações
var_btnConfig = driver.find_element(By.XPATH, '/html/body/header/div[2]/div[1]/div/div[3]/div[1]/div[1]/button')
var_btnConfig.click()

# Acessando aba de troca de moeda
var_btnTrocaMoeda = driver.find_element(By.XPATH, '/html/body/header/div[2]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[2]')
var_btnTrocaMoeda.click()

# Trocando a moeda para Real
var_btnRealBr = driver.find_element(By.XPATH, "//div[contains(@class, 'setting-item') and contains(@class, 'tw-flex')]//span[text()='Brazil Real']")
var_btnRealBr.click()
