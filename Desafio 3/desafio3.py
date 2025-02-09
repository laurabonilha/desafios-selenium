'''
PROPOSTA DO DESAFIO: UTILIZAR MULTIPLAS ABAS (DESAFIO 2 E DESAFIO 3), CADA UMA ACESSANDO UMA PÁGINA ESPECÍFICA. PRIMEIRAMENTE, A AUTOMAÇÃO DEVE ACESSAR A ABA REFERENTE AO DESAFIO 3 E 
CAPTURAR O NOME DO USUÁRIO QUE SERÁ PROCESSADO. EM SEGUIDA, DEVERÁ ACESSAR A ABA DO DESAFIO 2 E BUSCAR PELO NOME DO USUÁRIO. APÓS A PESQUISA, DEVE CAPTURAR TODOS OS DADOS DOS USUÁRIOS
RETORNADOS PELO SITE COM O NOME DE USUÁRIO E, POR FIM, DEVE ACESSAR NOVAMENTE A ABA DO DESAFIO 3 E PREENCHER OS DADOS CAPTURADOS CORRETAMENTE NO FORMULÁRIO, DE ACORDO COM A SUA CORRESPONDÊNCIA.
O PROCESSO DEVE SE REPETIR PARA TODOS OS USUÁRIOS FORNECIDOS PELA PÁGINA DA ABA DE DESAFIO 2 ATÉ QUE HAJA INDICAÇÃO DE QUE TODOS OS USUÁRIOS JÁ FORAM CAPTURADOS.
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
driver.get('https://curso-web-scraping.pages.dev/#/desafio/2')
driver.implicitly_wait(time_to_wait=10)
driver.maximize_window()

# Abrindo uma nova aba 
driver.switch_to.new_window('tab')
driver.get('https://curso-web-scraping.pages.dev/#/desafio/3')

# Ativando a aba do Desafio 3
for aba in driver.window_handles:
    driver.switch_to.window(aba)
    if 'Desafio 3' in driver.title:
        break

try:
    var_elementoUsuario = driver.find_element(By.ID, 'usuario')

    while var_elementoUsuario:
        var_strNomeUsuario = var_elementoUsuario.get_attribute('innerText')

        # Ativando a aba do Desafio 2
        for aba in driver.window_handles:
            driver.switch_to.window(aba)
            if 'Desafio 2' in driver.title:
                break

        # Buscando o usuário atual
        var_inputUsuario = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div[2]/input')
        var_inputUsuario.clear()
        var_inputUsuario.send_keys(var_strNomeUsuario)
        var_btnBuscar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/div[2]/button')
        var_btnBuscar.click()

        # Esperando aparecer a tabela para capturar os dados
        wait.until(EC.visibility_of_element_located(locator=(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/section/div/div[2]')))

        # Encontrando os usuários dentro da tabela
        var_listaUsuarios = driver.find_elements(By.CSS_SELECTOR, 'div.items-center.bg-gray-50')

        # Criando lista de usuários
        dados_usuarios = []

        #Loop ára capturar os dados de todos da lista de usuários da página
        for usuario_atual in var_listaUsuarios:
            var_strTextoUsuario = usuario_atual.get_attribute('innerText')
                
            # Função auxiliar para aplicar regex com verificação
            def extract_with_regex(pattern, text, group_index=0):
                match = re.search(pattern, text)
                return match.group(group_index).strip() if match else None

            # Aplica Regex para capturar as informações
            lines = var_strTextoUsuario.split('\n')
            
            # Nome é sempre a primeira linha
            var_strNomeUsuario = lines[0].strip() if len(lines) > 0 else None
            
            # Cargo é sempre a segunda linha
            var_strCargoUsuario = lines[1].strip() if len(lines) > 1 else None
            
            # Aplica Regex para capturar os dados (sem os prefixos)
            var_strEmailUsuario = extract_with_regex(r'(?<=E-mail:\s)([^\n]+)', var_strTextoUsuario)  
            var_strTelefoneUsuario = extract_with_regex(r'(?<=Telefone:\s)([^\n]+)', var_strTextoUsuario)  
            var_strUsuarioUsuario = extract_with_regex(r'(?<=Usuário:\s)([^\n]+)', var_strTextoUsuario)  
            var_strEstadoUsuario = extract_with_regex(r'(?<=Estado:\s)([^\n]+)', var_strTextoUsuario) 

            # Adiciona os dados do usuário ao dicionário
            dados_usuarios.append({
                "Nome": var_strNomeUsuario,
                "Cargo": var_strCargoUsuario,
                "E-mail": var_strEmailUsuario,
                "Telefone": var_strTelefoneUsuario,
                "Usuário": var_strUsuarioUsuario,
                "Estado": var_strEstadoUsuario
            })

        # Cria o DataFrame
        df_usuarios = pd.DataFrame(dados_usuarios)

        # Exibe o DataFrame
        print(df_usuarios)


        # Ativando a aba do desafio 3 e preenchendo os dados
        for aba in driver.window_handles:
            driver.switch_to.window(aba)
            if 'Desafio 3' in driver.title:
                break

        # Loop para preencher e enviar os dados de cada usuário
        for index, row in df_usuarios.iterrows():
            # Localiza e preenche os campos do formulário
            var_cadastroNome = driver.find_element(By.ID, 'radix-:r0:')
            var_cadastroNome.clear()
            var_cadastroNome.send_keys(row["Nome"])
            var_cadastroProfissao = driver.find_element(By.ID, 'radix-:r1:')
            var_cadastroProfissao.clear()
            var_cadastroProfissao.send_keys(row["Cargo"])
            var_cadastroEmail = driver.find_element(By.ID, 'radix-:r2:')
            var_cadastroEmail.clear()
            var_cadastroEmail.send_keys(row["E-mail"])
            var_cadastroTelefone = driver.find_element(By.ID, 'radix-:r3:')
            var_cadastroTelefone.clear()
            var_cadastroTelefone.send_keys(row["Telefone"])
            var_cadastroUsuario = driver.find_element(By.ID, 'radix-:r4:')
            var_cadastroUsuario.clear()
            var_cadastroUsuario.send_keys(row["Usuário"])
            var_cadastroEstado = Select(driver.find_element(By.NAME, 'estado'))
            var_cadastroEstado.select_by_visible_text(row["Estado"])  

            var_btnCadastrar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/form/button').click()

        # Após terminar um nome de usuário, verifica se há outro para processar
        var_btnCadastrar = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/main/div[2]/div/form/button').click()
except:
    print('Não há mais itens a serem processados')