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
import os
import requests

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

        # Captura o índice da criptomoeda no site
        var_elementoIndice = criptomoeda.find_element(By.XPATH, "//td[contains(@class, 'tw-sticky') and contains(@class, '2lg:tw-static') and contains(@class, 'tw-left-[24px]') and contains(@class, 'tw-px-1') and contains(@class, 'tw-py-2.5') and contains(@class, 'tw-bg-inherit') and contains(@class, 'tw-text-gray-900') and contains(@class, 'dark:tw-text-moon-50')]")
        var_strIndiceMoeda = var_elementoIndice.text

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

        # Encontra o elemento da variação em 1 hora
        var_elementoVariacao1Hora = criptomoeda.find_element(By.XPATH, ".//span[(contains(@class, 'gecko-up') or contains(@class, 'gecko-down')) and @data-attr='price_change_percentage_1h']")

        # Captura o valor da variação em 1 hora
        var_strVariacao1Hora = var_elementoVariacao1Hora.text.strip().replace("%", "").replace(",", ".")

        # Encontrar o elemento de positivo ou negativo dentro do span
        var_elementoSinalVariacao1Hora = var_elementoVariacao1Hora.find_element(By.XPATH, ".//i[contains(@class, 'fas') and contains(@class, 'fa-fw')]")

        # Verificar se a classe do i é 'fa-caret-up' ou 'fa-caret-down'
        if 'fa-caret-up' in var_elementoSinalVariacao1Hora.get_attribute('class'):
            indice = 1  # Índice positivo
        elif 'fa-caret-down' in var_elementoSinalVariacao1Hora.get_attribute('class'):
            indice = -1  # Índice negativo
        else:
            indice = 0  # Caso não encontre, assume 0

        # Converter a variação para float e aplicar o sinal
        try:
            var_Variacao1Hora = float(var_strVariacao1Hora) * indice
        except ValueError:
            var_Variacao1Hora = 0  # Se não conseguir converter, assume 0

        # Captura o elemento da variação em 24 horas
        var_elementoVariacao24Horas = criptomoeda.find_element(By.XPATH, ".//span[(contains(@class, 'gecko-up') or contains(@class, 'gecko-down')) and @data-attr='price_change_percentage_24h']")

        # Captura o valor da variação em 24 horas
        var_strVariacao24Horas = var_elementoVariacao24Horas.text.strip().replace("%", "").replace(",", ".")

        # Encontra se a variação em 24 horas é positiva ou negativa
        var_elementoSinalVariacao24Horas = var_elementoVariacao24Horas.find_element(By.XPATH, ".//i[contains(@class, 'fas') and contains(@class, 'fa-fw')]")
        
        # Verificar se a classe do i é 'fa-caret-up' ou 'fa-caret-down'
        if 'fa-caret-up' in var_elementoSinalVariacao24Horas.get_attribute('class'):
            indice = 1  # Índice positivo
        elif 'fa-caret-down' in var_elementoSinalVariacao24Horas.get_attribute('class'):
            indice = -1  # Índice negativo
        else:
            indice = 0  # Caso não encontre, assume 0

        # Converter a variação para float e aplicar o sinal
        try:
            var_Variacao24Horas = float(var_strVariacao24Horas) * indice
        except ValueError:
            var_Variacao24Horas = 0  # Se não conseguir converter, assume 0

        # Captura o elemento de variação em 7 dias
        var_elementoVariacao7Dias = criptomoeda.find_element(By.XPATH, ".//span[(contains(@class, 'gecko-up') or contains(@class, 'gecko-down')) and @data-attr='price_change_percentage_7d']")
        
        # Captura o valor da variação em 7 dias
        var_strVariacao7Dias = var_elementoVariacao7Dias.text.strip().replace("%", "").replace(",", ".")
        
        # Encontra se a variação em 7 dias é negatia ou positiva
        var_elementoSinalVariacao7Dias = var_elementoVariacao7Dias.find_element(By.XPATH, ".//i[contains(@class, 'fas') and contains(@class, 'fa-fw')]")

        # Verificar se a classe do i é 'fa-caret-up' ou 'fa-caret-down'
        if 'fa-caret-up' in var_elementoSinalVariacao7Dias.get_attribute('class'):
            indice = 1  # Índice positivo
        elif 'fa-caret-down' in var_elementoSinalVariacao7Dias.get_attribute('class'):
            indice = -1  # Índice negativo
        else:
            indice = 0  # Caso não encontre, assume 0

        # Converter a variação para float e aplicar o sinal
        try:
            var_Variacao7Dias = float(var_strVariacao7Dias) * indice
        except ValueError:
            var_Variacao7Dias = 0  # Se não conseguir converter, assume 0

        # Encontra o elemento de volume em 24 horas
        var_elementoVolume = criptomoeda.find_element(By.XPATH, "//td[@class='tw-text-end tw-px-1 tw-py-2.5 2lg:tw-p-2.5 tw-bg-inherit tw-text-gray-900 dark:tw-text-moon-50']")
        var_strVolume = var_elementoVolume.text

        # Encontra o elemento Capitalização de mercado
        var_elementoCapitalizacao = criptomoeda.find_element(By.XPATH, "//td[@class='tw-text-end tw-px-1 tw-py-2.5 2lg:tw-p-2.5 tw-bg-inherit tw-text-gray-900 dark:tw-text-moon-50']")
        var_strCapitalizacao = var_elementoCapitalizacao.text

        # Captura os links da imagens - gráfico últimos 7 dias
        var_elementoGrafico = criptomoeda.find_element(By.XPATH, "//td[contains(@class, 'tw-text-end') and contains(@class, 'tw-box-content')]//img")
        var_strLinkGrafico = var_elementoGrafico.get_attribute('src')

        # Salva as imagens dos gráficos numa pasta da automação
        var_dirGraficos = 'Gráficos'

        # Verifica se a pasta local para salvar os gráficos existe e, se não existir, cria ela
        if not os.path.exists(var_dirGraficos):
            os.makedirs(var_dirGraficos)

        # Se existir gráfico, faz o download
        if var_strLinkGrafico:
            try:
                response = requests.get(var_strLinkGrafico, stream=True)
                response.raise_for_status()  # Verifica se houve erro no download

                # Determinar a extensão do arquivo
                ext = ".jpg" if "jpeg" in response.headers["Content-Type"] else ".png"

                # Criar o caminho para salvar a imagem
                caminho_arquivo = os.path.join(var_dirGraficos, f"grafico_{var_strNomeMoeda}{var_strTipoMoeda}")

                # Salvar a imagem no arquivo
                with open(caminho_arquivo, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)

            except requests.exceptions.RequestException as e:
                print(f"Erro ao baixar {caminho_arquivo}: {e}")

        
