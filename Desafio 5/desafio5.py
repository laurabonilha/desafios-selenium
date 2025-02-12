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

driver.maximize_window()

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

# Alterando url para capturar 300 itens por página
driver.get('https://www.coingecko.com/pt?items=300')

# Aguardando o carregamento completo da tabela de resultados
wait.until(EC.presence_of_element_located(locator=(By.XPATH, '/html/body/div[2]/main/div/div[5]/table')))

# Encontrando todas as linhas de criptomoedas
var_linhasCripto = driver.find_elements(By.XPATH, "//tr[contains(@class, 'tw-bg-white') and contains(@class, 'tw-text-sm')]")

# Loop para capturar os dados em todas as páginas

while True:
    for criptomoeda in var_linhasCripto:
        # Captura o nome completo da moeda (incluindo o tipo)
        var_strElementoMoeda = criptomoeda.find_element(By.XPATH, ".//div[contains(@class, 'tw-text-gray-700')]")
        var_strMoedaCompleto = var_strElementoMoeda.text.strip()

        # Captura o tipo da moeda
        try:
            var_elementoTipoMoeda = criptomoeda.find_element(By.XPATH, ".//div[contains(@class, 'tw-block')]")
            var_strTipoMoeda = var_elementoTipoMoeda.text.strip()
        except:
            var_strTipoMoeda = ""  # Se não encontrar o tipo, define como string vazia

        # Remove o tipo da moeda apenas se estiver no final do nome (mesmo nome e tipo)
        if var_strTipoMoeda and var_strMoedaCompleto.endswith(var_strTipoMoeda):
            var_strNomeMoeda = re.sub(r"\b" + re.escape(var_strTipoMoeda) + r"\b\s*$", "", var_strMoedaCompleto).strip()
        else:
            var_strNomeMoeda = var_strMoedaCompleto  # Mantém o nome inalterado

        # Verifica se há elemento de compra no site
        var_elementoCompra = criptomoeda.find_element(By.XPATH, ".//td[contains(@class, '!tw-p-0') and contains(@class, 'tw-px-1') and contains(@class, 'tw-py-2.5')]")

        try:
            # Verifique se há um <div> dentro do <td>
            var_elementoDivCompra = var_elementoCompra.find_element(By.XPATH, ".//div")
            var_admiteCompra = True
        except:
            var_admiteCompra = False

        # Captura o preço da moeda
        var_strPrecoMoeda = criptomoeda.find_element(By.XPATH, ".//td[contains(@class, 'tw-text-end') and contains(@class, 'tw-px-1') and contains(@class, 'tw-text-gray-900')]").text

        # Captura a variação em 1 hora
        var_variacao1Hora = criptomoeda.find_element(By.XPATH, ".//span[contains(@class, 'gecko-up')]").text
        
        




        


