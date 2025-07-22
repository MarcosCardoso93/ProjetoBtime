import requests
import pandas as pd

class ApiFipe:
    def __init__(self):
        self.lista = pd.read_csv('listaFipe.csv', sep=";")
        self.DataFrame = pd.DataFrame({"FIPE":[],"MARCA":[],"MODELO":[],"ANO MODELO":[],"MES REFERENCIA":[],"VALOR":[]})

    def consultar_codigo_fipe(self,codigo_fipe):
        url = f"https://brasilapi.com.br/api/fipe/preco/v1/{codigo_fipe}"
        response = requests.get(url)

        if response.status_code == 200:
            dados = response.json()
            return dados[0]
        else:
            print("Erro ao consultar a API:", response.status_code)
            return {}

    def preencherDataFrame(self,fipe,retorno):
        try:
            
            if retorno:
                valor = retorno["valor"]
                marca = retorno["marca"]
                modelo = retorno["modelo"]
                anoModelo = retorno["anoModelo"]
                mesReferencia = retorno["mesReferencia"]
            else:
                valor,marca,modelo,anoModelo,mesReferencia = "","","","",""
            ultimaLinha = self.DataFrame.shape[0]
            self.DataFrame.loc[ultimaLinha,"FIPE"] = str(fipe)
            self.DataFrame.loc[ultimaLinha,"MARCA"] = marca
            self.DataFrame.loc[ultimaLinha,"MODELO"] = modelo
            self.DataFrame.loc[ultimaLinha,"ANO MODELO"] = str(int(anoModelo))
            self.DataFrame.loc[ultimaLinha,"MES REFERENCIA"] = mesReferencia
            self.DataFrame.loc[ultimaLinha,"VALOR"] = valor

        except Exception as erro:
            print("erro inserir valores!")

    def SalvarCsv(self):
        try:
            self.DataFrame.to_csv("RetornoConsultaApi.csv", index=False,sep=',')
        except:
            print("erro em salvar planilha csv!")

def main():           
    fipeApi = ApiFipe()
    listaFipe = fipeApi.lista
    for _, linha in listaFipe.iterrows():
        codigoFipe = linha[0].strip()
        retorno = fipeApi.consultar_codigo_fipe(codigoFipe)
        fipeApi.preencherDataFrame(codigoFipe,retorno)
    fipeApi.SalvarCsv()

if __name__ == '__main__':
    main()