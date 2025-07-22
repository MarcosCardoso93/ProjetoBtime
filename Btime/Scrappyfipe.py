import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import json
import time



class FipeScrappySite:
    def __init__(self):
        self.link = "https://veiculos.fipe.org.br/"
        self.lista = pd.read_csv('listaFipe.csv', sep=";")
        self.DataFrame = pd.DataFrame({"FIPE":[],"MARCA":[],"MODELO":[],"ANO MODELO":[],"MES REFERENCIA":[],"VALOR":[]})
        # Configurações do Edge (opcional)
        options = Options()
        options.add_argument("--start-maximized")  # Tela cheia
        # options.add_argument("--headless")  # Descomente se não quiser abrir a janela
        service = EdgeService(executable_path="msedgedriver.exe")
        try:
            self.driver = webdriver.Edge(options=options,service=service)
            self.wait = WebDriverWait(self.driver, 15)
        except WebDriverException as e:
            print("Erro ao iniciar o navegador:", e)
            raise

    def AcessarSite(self):
        try:
            self.driver.get(self.link)
            # Aguarda até que o elemento principal da página esteja disponível
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Consulta de Carros e Utilitários Pequenos')]")))
            return True
        except TimeoutException:
            print("Tempo excedido ao tentar carregar a página FIPE.")
            return False
        except WebDriverException as e:
            print("Erro ao acessar o site:", e)
            return False

    def PesquisarCarros(self, codigoFipe):
        try:
            self.driver.get(self.link)
            time.sleep(3)
            # acessa a opção Consulta de Carros e Utilitários Pequenos
            consultaCarros = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Consulta de Carros e Utilitários Pequenos')]"))
            )
            
            consultaCarros.click()
            time.sleep(2)
            # acessa a opção Pesquisa por código Fipe
            pesquisaCodigo = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Pesquisa por código Fipe')]"))
            )
            pesquisaCodigo.click()
            time.sleep(2)
            # pesquisa pelo codigoFipe
            inputCodigo = self.wait.until(
                EC.presence_of_element_located((By.ID, "selectCodigocarroCodigoFipe"))
            )
            inputCodigo.clear()
            inputCodigo.send_keys(codigoFipe)
            self.driver.execute_script("arguments[0].blur();", inputCodigo)
            time.sleep(5)
            
            # Selecionar a ultima opção disponível  de ano modelo 
            try:#padrão do site número 1
                dropdown_visible = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "selectCodigoAnocarroCodigoFipe_chosen")))
                dropdown_visible.click()
                primeiro_item = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//ul[@class='chosen-results']/li[1]"))
                )
                primeiro_item.click()
            except:
                pass
            try:#padrão do site número 2
                select = Select(self.wait.until(EC.presence_of_element_located((By.ID, "selectCodigoAnocarroCodigoFipe"))))
                select.select_by_value(next(opt.get_attribute("value") for opt in select.options if opt.get_attribute("value").strip()))
            except:
                pass

            time.sleep(2)
            botaoPesquisar = self.wait.until(
                EC.element_to_be_clickable((By.ID, "buttonPesquisarcarroPorCodigoFipe"))
            )
            #clica em pesquisar
            botaoPesquisar.click()
            try: #tenta encontrar o elemento, se for Encontrado chama a função TratarResultado e retorna o resultado
                resultado = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div#resultadocarroCodigoFipe'))
                )
                print("Elemento encontrado.")
                resultado = self.TratarResultado()
                return resultado
            except TimeoutException: # excessão de timeout (não encontrou o elemento)
                print("Elemento não encontrado (timeout).")
                return {}

        except TimeoutException: # excessão de timeout na tela
            print(f"Tempo excedido ao tentar pesquisar o código FIPE: {codigoFipe}")
            return {}
        except NoSuchElementException as e: #excessão de elemento não encontrado 
            print(f"Elemento não encontrado durante a pesquisa: {e}")
            return {}
        except Exception as erro: #erro não esperado
            print(f"Erro inesperado na pesquisa: {erro}")
            return {}

    def TratarResultado(self):
        try:
            resultado = self.driver.find_element(By.CSS_SELECTOR,'div#resultadocarroCodigoFipe')
            # Extrai o HTML interno da tabela
            html_tabela = resultado.get_attribute("innerHTML")
            # Converte para DataFrame
            tabela_df = pd.read_html(html_tabela)[0]
            # transforma o dataFrame em dicionário 
            dados_dict = {row[0].replace(":", "").strip(): row[1] for _, row in tabela_df.iterrows()}
            json_str = json.dumps(dados_dict, ensure_ascii=False)
            return json_str
        except:
            return {}
            
    def preencherDataFrame(self,fipe,retorno):
        try:
            if retorno:#se for verdadeiro atribui valor as variáveis
                retorno = json.loads(retorno)
                valor = retorno["Preço Médio"]
                marca = retorno["Marca"]
                modelo = retorno["Modelo"]
                anoModelo = retorno["Ano Modelo"]
                mesReferencia = retorno["Mês de referência"]
            else:# senão atribui vazio as variáveis
                valor,marca,modelo,anoModelo,mesReferencia = "","","","",""
            ultimaLinha = self.DataFrame.shape[0]
            self.DataFrame.loc[ultimaLinha,"FIPE"] = str(fipe)
            self.DataFrame.loc[ultimaLinha,"MARCA"] = marca
            self.DataFrame.loc[ultimaLinha,"MODELO"] = modelo
            self.DataFrame.loc[ultimaLinha,"ANO MODELO"] = anoModelo
            self.DataFrame.loc[ultimaLinha,"MES REFERENCIA"] = mesReferencia
            self.DataFrame.loc[ultimaLinha,"VALOR"] = valor

        except Exception as erro:
            print("erro inserir valores!")

    def SalvarCsv(self):
        try:
            self.DataFrame.to_csv("RetornoConsultaSite.csv", index=False,sep=',')
        except:
            print("erro em salvar planilha csv!")
def main():
    scrappy = FipeScrappySite()
    sucesso = False
    for tentativa in range(10):
        if scrappy.AcessarSite():
            sucesso = True
            break
    if not sucesso:
        print("Não foi possível acessar o site após várias tentativas.")
        return
        
    listaFipe = scrappy.lista
    for _, linha in listaFipe.iterrows():
        codigoFipe = linha[0].strip()
        retorno = scrappy.PesquisarCarros(codigoFipe=codigoFipe)
        scrappy.preencherDataFrame(codigoFipe,retorno)
    scrappy.SalvarCsv()
if __name__ == '__main__':
    main()


    