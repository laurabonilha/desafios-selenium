'''
    PROPOSTA DO DESAFIO:
    CONSTRUINDO UMA AUTOMAÇÃO UTILIZANDO SELENIUM QUE CAPTURA DADOS DE DIVERSOS USUÁRIOS(EMAIL, SENHA, DATA DE NASCIMENTO E SE RECEBERÁ NEWSLETTER) E 
    PREENCHE UM FORMULÁRIO QUE CONTEM CAMPOS DE INPUT, DE SELEÇÃO DE ELEMENTOS, BOTÃO QUE PODE SER HABILITADO OU DESABILITADO E ENVIA AO FINAL PRESSIONANDO O BOTÃO DE ENVIAR.

'''

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime

driver = webdriver.Chrome()
driver.get('https://curso-web-scraping.pages.dev/#/desafio/1')
driver.maximize_window()

# with - garante que o arquivo seja fechado após o bloco de código ser executado - poderia ser usado file.close()
# as file: cria uma variável chamada file que representa o arquivo aberto.
# Open - abre a arquivo
# 'r' - modo de leitura r
# parâmetro 'utf-8' - garante que o python leia o arquivo no formato UFT-8, essencial para lidar com caracteres especiais como acentos.
with open ('desafio_1.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)

var_numeroUsuario = 1
var_intContador = 0


for usuario in dados:

    # Preenchendo o e-mail
    print (f'Preenchendo os dados do usuário de número {var_numeroUsuario}')
    var_emailUser = usuario['email']
    var_inputEmail = driver.find_element(By.XPATH, '//*[@id="radix-:r0:"]')
    var_inputEmail.clear()
    var_inputEmail.send_keys(var_emailUser)
    print("Preencheu o email: " + var_emailUser)

    # Preenchendo a senha
    print(f'Inserindo a senha do usuário de número {var_numeroUsuario}')
    var_senhaUser = usuario['senha']
    var_inputSenha = driver.find_element(By.XPATH, '//*[@id="radix-:r1:"]')
    var_inputSenha.clear()
    var_inputSenha.send_keys(var_senhaUser)
    print("Preencheu a senha: " + var_senhaUser)

    # Preenchendo o dia do nascimento
    var_dataUser = datetime.strptime(usuario['data-de-nascimento'], '%Y-%m-%d')
    var_diaUser = var_dataUser.strftime('%d')
    var_diaUser_int = int(var_diaUser)
    var_selectDia = Select(driver.find_element(By.NAME, 'dia'))
    var_selectDia.select_by_visible_text(str(var_diaUser_int))

    # Preenchendo o mês do nascimento
    var_mesUser = var_dataUser.strftime('%m')
    var_mesUser_int = int(var_mesUser)
    var_indexMes = var_mesUser_int - 1
    var_selectMes = Select(driver.find_element(By.NAME, 'mes'))
    var_selectMes.select_by_index(var_indexMes)

    #Prenchendo ano de nascimento
    var_anoUser = var_dataUser.strftime('%Y')
    var_selectAno = Select(driver.find_element(By.NAME, 'ano'))
    var_selectAno.select_by_visible_text(var_anoUser)

    # Ativa/desativa a newsletter
    var_checkNews = driver.find_element(By.XPATH, '//*[@id="airplane-mode"]')
    var_estadoNews = var_checkNews.get_attribute("data-state")
    var_switchOn = True if var_estadoNews == 'checked' else False
    var_NewsUser = usuario['newsletter']

    if var_switchOn != var_NewsUser:
        var_checkNews.click()

    # Clicando no botão de enviar ao final do processamento
    var_botaoEnviar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/form/button')
    var_botaoEnviar.click()

    var_numeroUsuario += 1
    var_intContador += 1

print(f'Fim do processamento, processou {var_intContador} contas')