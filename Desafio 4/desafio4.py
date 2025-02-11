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
import time
import json

driver = webdriver.Chrome()
# Criando uma variável de espera padrão
wait = WebDriverWait(driver=driver, timeout=15, poll_frequency=1)
driver.get('https://curso-web-scraping.pages.dev/#/desafio/4')
driver.implicitly_wait(time_to_wait=10)
driver.maximize_window()


# Criando uma lista com os itens a serem processados
var_listItensProcessar = ['celulares', 'tvs', 'games', 'notebooks']
produtosEncontrados = []


for item in var_listItensProcessar:
    # Criando diferentes tratativas a depender do item a ser processado
    match(item):
        case 'celulares':
            #Acessando diretamente a URL dos celulares
            driver.get('https://curso-web-scraping.pages.dev/#/desafio/4?categoria=celulares')
            # Verifica se a aba lateral está aberta e se estiver fecha
            try:
                var_elementSideBar = driver.find_element(By.XPATH, '//*[@id="default-sidebar"]/div')
                if var_elementSideBar:
                    print("Barra lateral está aberta, fechando...")
                    var_btnSideBar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/button')
            except:
                print("Barra lateral não está aberta. Seguindo")
            var_tblFiltros = driver.find_element(By.XPATH, '//*[@id="filtros"]/div/div[1]/div[1]')
            wait.until(EC.presence_of_element_located(locator=(By.ID, 'frete')))
            time.sleep(1)
            var_selectFreteGratis = driver.find_element(By.ID, 'frete')
            var_selectFreteGratis.click()
            time.sleep(1)
            # Selecionando oferta
            var_selectOferta = driver.find_element(By.ID, 'oferta')
            var_selectOferta.click()
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

            while True:

                # Capturando todos os produtos da primeira página
                var_elementoProdutos = driver.find_elements(By.CSS_SELECTOR, 'div.border-gray-200.rounded-lg')

                for produto in var_elementoProdutos:
                    var_strNomeProduto = produto.find_element(By.XPATH, './/h5[contains(@class, "text-xl")]').text
                    var_strDescricaoProduto = produto.find_element(By.XPATH, './/div[contains(@class, "text-ellipsis") and contains(@class, "line-clamp-3")]').text
                    var_strPrecoProduto = produto.find_element(By.XPATH, './/div[@class="grow"]//span[contains(@class, "text-3xl") and contains(@class, "font-bold")]').text
                    
                    # Adiciona os produtos encontrados numa lista
                    produtosEncontrados.append({
                        "NOME DO PRODUTO": var_strNomeProduto,
                        "DESCRIÇÃO": var_strDescricaoProduto,
                        "PREÇO": 'R$' + var_strPrecoProduto
                    })

                try:
                    # Verifica se o botão de próxima página está habilitado
                    var_btnProximaPagina = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[2]/button[2]')
                    # Se o botão estiver habilitado, encerra o loop
                    if var_btnProximaPagina.get_attribute('disabled'):
                        print("Não há mais página para processar")
                        driver.refresh()
                        break
                    # Se o botão estiver disponível, clica e repete o processo para a próxima página
                    var_btnProximaPagina.click()
                except:
                    break    

        case 'tvs':
            #Acessando diretamente a URL das tvs
            driver.get('https://curso-web-scraping.pages.dev/#/desafio/4?categoria=tvs')
            # Verifica se a aba lateral está aberta e se estiver fecha
            try:
                var_elementSideBar = driver.find_element(By.XPATH, '//*[@id="default-sidebar"]/div')
                if var_elementSideBar:
                    print("Barra lateral está aberta, fechando...")
                    var_btnSideBar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/button')
            except:
                print("Barra lateral não está aberta. Seguindo")
            driver.implicitly_wait(time_to_wait=10)
            time.sleep(1)
            # Selecionando envio internacional
            var_selectEnvioInter = driver.find_element(By.ID, 'envio-internacional')
            var_selectEnvioInter.click()
            time.sleep(1)
            # Definindo o preço mínimo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_minimo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('0')
            # Definindo o preço máximo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_maximo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('5000')
            # Definindo 4 estrelas de avaliação
            var_selectQuatroEstrelas = driver.find_element(By.ID, 'five-stars')
            var_selectQuatroEstrelas.click()
            # Clicando no botão de busca
            var_btnBuscar = driver.find_element(By.XPATH, '//*[@id="filtros"]/div/div[2]/button[2]')
            var_btnBuscar.click()

            # Espera aparecer a tabela com os resultados
            wait.until(EC.visibility_of_element_located(locator=(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[1]')))

            while True:

                # Capturando todos os produtos da primeira página
                var_elementoProdutos = driver.find_elements(By.CSS_SELECTOR, 'div.border-gray-200.rounded-lg')

                for produto in var_elementoProdutos:
                    var_strNomeProduto = produto.find_element(By.XPATH, './/h5[contains(@class, "text-xl")]').text
                    var_strDescricaoProduto = produto.find_element(By.XPATH, './/div[contains(@class, "text-ellipsis") and contains(@class, "line-clamp-3")]').text
                    var_strPrecoProduto = produto.find_element(By.XPATH, './/div[@class="grow"]//span[contains(@class, "text-3xl") and contains(@class, "font-bold")]').text
                    
                    # Adiciona os produtos encontrados numa lista
                    produtosEncontrados.append({
                        "NOME DO PRODUTO": var_strNomeProduto,
                        "DESCRIÇÃO": var_strDescricaoProduto,
                        "PREÇO": 'R$' + var_strPrecoProduto
                    })

                try:
                    # Verifica se o botão de próxima página está habilitado
                    var_btnProximaPagina = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[2]/button[2]')
                    # Se o botão estiver habilitado, encerra o loop
                    if var_btnProximaPagina.get_attribute('disabled'):
                        print("Não há mais página para processar")
                        driver.refresh()
                        break
                    # Se o botão estiver disponível, clica e repete o processo para a próxima página
                    var_btnProximaPagina.click()
                except:
                    break    

        case 'games':
            #Acessando diretamente a URL de games
            driver.get('https://curso-web-scraping.pages.dev/#/desafio/4?categoria=games')
            # Verifica se a aba lateral está aberta e se estiver fecha
            try:
                var_elementSideBar = driver.find_element(By.XPATH, '//*[@id="default-sidebar"]/div')
                if var_elementSideBar:
                    print("Barra lateral está aberta, fechando...")
                    var_btnSideBar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/button')
            except:
                print("Barra lateral não está aberta. Seguindo")
            
            driver.implicitly_wait(time_to_wait=10)
            # Selecionando frete gratis
            var_selectFreteGratis = driver.find_element(By.ID, 'frete')
            var_selectFreteGratis.click()
            time.sleep(1)
            # Selecionando parcelamento sem juros
            var_selectParcelamento = driver.find_element(By.ID, 'parcelamento')
            var_selectParcelamento.click()
            time.sleep(1)
            # Definindo o preço mínimo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_minimo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('2000')
            # Definindo o preço máximo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_maximo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('8000')
            # Definindo 4 estrelas de avaliação
            var_selectQuatroEstrelas = driver.find_element(By.ID, 'three-stars')
            var_selectQuatroEstrelas.click()
            # Clicando no botão de busca
            var_btnBuscar = driver.find_element(By.XPATH, '//*[@id="filtros"]/div/div[2]/button[2]')
            var_btnBuscar.click()

            # Espera aparecer a tabela com os resultados
            wait.until(EC.visibility_of_element_located(locator=(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[1]')))

            while True:

                # Capturando todos os produtos da primeira página
                var_elementoProdutos = driver.find_elements(By.CSS_SELECTOR, 'div.border-gray-200.rounded-lg')

                for produto in var_elementoProdutos:
                    var_strNomeProduto = produto.find_element(By.XPATH, './/h5[contains(@class, "text-xl")]').text
                    var_strDescricaoProduto = produto.find_element(By.XPATH, './/div[contains(@class, "text-ellipsis") and contains(@class, "line-clamp-3")]').text
                    var_strPrecoProduto = produto.find_element(By.XPATH, './/div[@class="grow"]//span[contains(@class, "text-3xl") and contains(@class, "font-bold")]').text
                    
                    # Adiciona os produtos encontrados numa lista
                    produtosEncontrados.append({
                        "NOME DO PRODUTO": var_strNomeProduto,
                        "DESCRIÇÃO": var_strDescricaoProduto,
                        "PREÇO": 'R$' + var_strPrecoProduto
                    })

                try:
                    # Verifica se o botão de próxima página está habilitado
                    var_btnProximaPagina = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[2]/button[2]')
                    # Se o botão estiver habilitado, encerra o loop
                    if var_btnProximaPagina.get_attribute('disabled'):
                        print("Não há mais página para processar")
                        driver.refresh()
                        break
                    # Se o botão estiver disponível, clica e repete o processo para a próxima página
                    var_btnProximaPagina.click()
                except:
                    break    

        case 'notebooks':
            #Acessando diretamente a URL de notebooks
            driver.get('https://curso-web-scraping.pages.dev/#/desafio/4?categoria=notebooks')
            # Verifica se a aba lateral está aberta e se estiver fecha
            try:
                var_elementSideBar = driver.find_element(By.XPATH, '//*[@id="default-sidebar"]/div')
                if var_elementSideBar:
                    print("Barra lateral está aberta, fechando...")
                    var_btnSideBar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/button')
            except:
                print("Barra lateral não está aberta. Seguindo")
            
            driver.implicitly_wait(time_to_wait=10)
            time.sleep(1)
            # Selecionando oferta
            var_selectFreteGratis = driver.find_element(By.ID, 'oferta')
            var_selectFreteGratis.click()
            time.sleep(1)
            # Selecionando parcelamento sem juros
            var_selectParcelamento = driver.find_element(By.ID, 'parcelamento')
            var_selectParcelamento.click()
            time.sleep(1)
            # Definindo o preço mínimo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_minimo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('1234')
            # Definindo o preço máximo
            var_inputPrecoMinimo = driver.find_element(By.NAME, 'preco_maximo')
            var_inputPrecoMinimo.clear()
            var_inputPrecoMinimo.send_keys('7896')
            # Definindo 4 estrelas de avaliação
            var_selectQuatroEstrelas = driver.find_element(By.ID, 'four-stars')
            var_selectQuatroEstrelas.click()
            # Clicando no botão de busca
            var_btnBuscar = driver.find_element(By.XPATH, '//*[@id="filtros"]/div/div[2]/button[2]')
            var_btnBuscar.click()

            # Espera aparecer a tabela com os resultados
            wait.until(EC.visibility_of_element_located(locator=(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[1]')))

            while True:

                # Capturando todos os produtos da primeira página
                var_elementoProdutos = driver.find_elements(By.CSS_SELECTOR, 'div.border-gray-200.rounded-lg')

                for produto in var_elementoProdutos:
                    var_strNomeProduto = produto.find_element(By.XPATH, './/h5[contains(@class, "text-xl")]').text
                    var_strDescricaoProduto = produto.find_element(By.XPATH, './/div[contains(@class, "text-ellipsis") and contains(@class, "line-clamp-3")]').text
                    var_strPrecoProduto = produto.find_element(By.XPATH, './/div[@class="grow"]//span[contains(@class, "text-3xl") and contains(@class, "font-bold")]').text
                    
                    # Adiciona os produtos encontrados numa lista
                    produtosEncontrados.append({
                        "NOME DO PRODUTO": var_strNomeProduto,
                        "DESCRIÇÃO": var_strDescricaoProduto,
                        "PREÇO": 'R$' + var_strPrecoProduto
                    })

                try:
                    # Verifica se o botão de próxima página está habilitado
                    var_btnProximaPagina = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div/div/div[2]/button[2]')
                    # Se o botão estiver habilitado, encerra o loop
                    if var_btnProximaPagina.get_attribute('disabled'):
                        print("Não há mais página para processar")
                        driver.refresh()
                        break
                    # Se o botão estiver disponível, clica e repete o processo para a próxima página
                    var_btnProximaPagina.click()
                except:
                    break    

# Criando um dataframe para armazenar os dados capturados
df_produtosEncontrados = pd.DataFrame(produtosEncontrados)

df_produtosEncontrados.to_excel("produtos.xlsx", index=False)

# Salvando os produtos em JSON
with open("produtos.json", "w", encoding="utf-8") as arquivo_json:
    json.dump(produtosEncontrados, arquivo_json, ensure_ascii=False, indent=4)