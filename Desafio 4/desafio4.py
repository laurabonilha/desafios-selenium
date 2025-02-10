'''
PROPOSTA DO DESAFIO: ACESSAR PÁGINA DO DESAFIO 4 QUE SIMULA UMA PÁGINA DE E-COMMERCE, QUE POSSUI DIVERSAS OPÇÕES DE FILTRO PARA MOSTRAR OS PRODUTOS.
A AUTOMAÇÃO DEVERÁ:
- SELECIONAR TODOS OS PRODUTOS DA CATEGORIA CELULARES COM FRETE GRÁTIS, EM OFERTA, PREÇO ENTRE R$ 500,00 - R$ 2.500,00 E COM 4 ESTRELAS DE AVALIAÇÃO
- SELECIONAR TODOS OS PRODUTOS DA CATEGORIA TVS COM ENVIO INTERNACIONAL, PREÇO ATÉ R$ 5.000,00 E 5 ESTRELAS
- SELECIONAR TODOS OS PRODUTOS DA CATEGORIA GAMES COM PARCELAMENTO SEM JUROS, FRETE GRÁTIS, PREÇO ENTRE R$ 2.000,00 E R$ 8.000,00 E 3 ESTRELAS
- SELECIONAR TODOS OS PRODUTOS DA CATEGORIA NOTEBOOKS COM PARCELAMENTO SEM JUROS, EM OFERTA, PREÇO ENTRE R$ 1.234,00 E R$ 7.896,00 E 4 ESTRELAS
- EXPORTAR TODOS OS DADOS COLETADOS PARA UM JSON E UM CSV
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select #seleção de campos web
import re
import pandas as pd

driver = webdriver.Chrome()
# Criando uma variável de espera padrão
wait = WebDriverWait(driver=driver, timeout=15, poll_frequency=1)
driver.get('https://curso-web-scraping.pages.dev/#/desafio/4')
driver.implicitly_wait(time_to_wait=10)
driver.maximize_window()


# Criando uma lista com os itens a serem processados
var_listItensProcessar = ['celulares', 'tvs', 'games', 'notebooks']

for item in var_listItensProcessar:
    # Criando diferentes tratativas a depender do item a ser processado
    match(item):
        case 'celulares':
            #Acessando diretamente a URL dos celulares
            driver.get('https://curso-web-scraping.pages.dev/#/desafio/4?categoria=celulares')
            var_tblFiltros = driver.find_element(By.XPATH, '//*[@id="filtros"]/div/div[1]/div[1]')
            # Selecionando frete gratis
            var_selectFreteGratis = driver.find_element(By.ID, 'frete')
            var_selectFreteGratis.click()
            # Selecionando oferta
            var_selectFreteGratis = driver.find_element(By.ID, 'oferta')
            var_selectFreteGratis.click()
            # Definindo o preço mínimo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_minimo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('500')
            # Definindo o preço máximo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_maximo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('2500')
            # Definindo 4 estrelas de avaliação
            var_selectQuatroEstrelas = driver.find_element(By.ID, 'four-stars')
            var_selectQuatroEstrelas.click()
            # Clicando no botão de busca
            var_btnBuscar = driver.find_element(By.XPATH, '//*[@id="filtros"]/div/div[2]/button[2]')
            var_btnBuscar.click()

            # Espera aparecer a tabela com os resultados
            wait.until(EC.visibility_of_element_located(locator=(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[1]')))

            # Capturando todos os produtos da primeira página
            var_elementoProdutos = driver.find_elements(By.CSS_SELECTOR, 'form#filtros + div div:has(>img)')

            for produto in var_elementoProdutos:
                var_strInfoProduto = produto.get_attribute('innerText')

             # Aplica Regex para capturar as informações
            lines = var_strInfoProduto.split('\n')
            
            # Nome do produto é sempre a primeira linha
            var_strNomeProduto = lines[0].strip() if len(lines) > 0 else None
            
            # Verificando se há mais página para buscar
            var_btnProximaPagina = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[2]/button[2]')
            var_ultimaPagina = var_btnProximaPagina.get_attribute('disabled')

            # Verifica se é a última página e se não for continua capturando os dados da próximas
            while not var_ultimaPagina:
                var_btnProximaPagina.click()
                produtos = driver.find_elements(By.CSS_SELECTOR, 'form#filtros + div div:has(>img)')
            


        
        case 'tvs':
            pass

        case 'games':
            pass

        case 'notebooks':
            pass