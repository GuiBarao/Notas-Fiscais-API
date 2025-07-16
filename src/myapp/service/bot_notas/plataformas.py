from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import (
    NoSuchElementException, StaleElementReferenceException, 
    TimeoutException, WebDriverException, ElementNotInteractableException
)
import time

class Plataforma:
    url: str
    usuario: str
    senha: str
    navegador: webdriver
    waitDriver: WebDriverWait
    
    def __init__(self, url:str, usuario:str, senha:str):
        self.url = url
        self.usuario = usuario
        self.senha = senha
    
    def login(self, dados_adicionais) -> bool:
        pass
    
    def emitir(self, nota, dados_adicionais) -> None:
        pass
    
    def cadastrar_tomador(self, nota, dados_adicionais) -> None:
        pass
    
    def formatar_valor(self, valor) -> str:
        pass

#
class Agile(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)
    
    def login(self, dados_adicionais = {}) -> bool:
        try:
            # Constantes para localização de elementos
            NFSE_BUTTON_XPATH = '/html/body/div[2]/div[2]/div[5]'
            USUARIO_INPUT_XPATH = '//*[@id="textfield-1015-inputEl"]'
            SENHA_INPUT_XPATH = '//*[@id="textfield-1017-inputEl"]'
            LOGIN_BUTTON_XPATH = '//*[@id="button-1049"]'
            PRESTADOR_INPUT_XPATH = '//*[@id="aglcombobox-1067-inputEl"]'
            COMPETENCIA_BUTTON_XPATH = '//*[@id="aglcombobox-1071-inputEl"]'
            MENU_INPUT_XPATH = '//*[@id="button-1074"]'
            
            MENU_CSS_CLASS = f'[data-recordid="{dados_adicionais["menu_emissao"]}"]'
            
            # Seleciona o módulo de NFS-e
            buttonNfse = self.wait.until(
                EC.presence_of_element_located((By.XPATH, NFSE_BUTTON_XPATH))
            )
            buttonNfse.click()

            # Preenche as informações para login
            inputUsuario = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            )
            inputUsuario.send_keys(self.usuario)
            
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            buttonLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()

            time.sleep(3)
            
            # Seleciona o prestador dos serviços
            inputPrestador = self.wait.until(
                EC.presence_of_element_located((By.XPATH, PRESTADOR_INPUT_XPATH))
            )
            inputPrestador.clear()
            inputPrestador.send_keys(dados_adicionais['cnpj'])
            time.sleep(1)
            inputPrestador.send_keys(Keys.TAB)
            
            time.sleep(1)
            
            buttonCompetencia = self.wait.until(
                EC.presence_of_element_located((By.XPATH, COMPETENCIA_BUTTON_XPATH))
            )
            buttonCompetencia.click()

            time.sleep(3)
            
            # Seleciona no menu a opção de notas
            inputMenuNfse = self.wait.until(
                EC.presence_of_element_located((By.XPATH, MENU_INPUT_XPATH))
            )
            inputMenuNfse.send_keys('Emissão de NFS-e por competência')

            time.sleep(2)
            
            buttonMenuNfse = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, MENU_CSS_CLASS))
            )
            buttonMenuNfse.click()  
            
            time.sleep(15)
            
            buttonNovaNota = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Nova')
            buttonNovaNota.click()
        
            return True

        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
            
    def emitir(self, nota, dados_adicionais) -> None:
        try: 
            time.sleep(5)

            buttonMenuTomador = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Tomador serviço')
            buttonMenuTomador.click()

            time.sleep(1)
            
            input_tomador = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'IdPessoaTomador'))
            )
            input_tomador.send_keys(nota["CPF_CNPJ"])
            time.sleep(4)
            input_tomador.send_keys(Keys.TAB)
            time.sleep(4)
        
            if not input_tomador.get_attribute('value'):
                raise Exception('Tomador não cadastrado')
            else:
                pass
            
            buttonServico = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Serviços')
            buttonServico.click()
            
            time.sleep(1)
            
            buttonInserir = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Inserir')
            buttonInserir.click()
            
            time.sleep(1)
            
            inputDescricao = self.navegador.find_element(By.NAME, 'Servico')
            inputDescricao.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")
            
            time.sleep(1)
            
            inputCnae = self.navegador.find_element(By.NAME, 'IdEstruturaPadraoCNAE')
            inputCnae.click()
            
            time.sleep(1)
            
            inputCnae.send_keys('96.0.3-3.99')
            
            time.sleep(2)
            
            ActionChains(self.navegador)\
                .move_to_element(inputCnae)\
                .click()\
                .perform()

            time.sleep(1)

            ActionChains(self.navegador)\
                .move_by_offset(0, 45)\
                .click()\
                .perform()
                
            time.sleep(3)
            
            inputQuantidade = self.navegador.find_element(By.NAME, 'Quantidade')
            inputQuantidade.send_keys(1)
            
            inputValor = self.navegador.find_element(By.NAME, 'ValorUnitario')
            inputValor.send_keys(self.formatar_valor(nota["VALOR"]))
            inputValor.send_keys(Keys.TAB)
            
            time.sleep(1)
            
            buttonConfirmar = self.navegador.find_element(By.PARTIAL_LINK_TEXT, "Confirmar")
            buttonConfirmar.click()
            
            time.sleep(2)
            
            buttonSalvar = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Salvar')
            buttonSalvar.click()
            
            time.sleep(10)
            
            buttonNovaNota = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Nova')
            buttonNovaNota.click()
            
            return True
        except Exception as e:
            try:
                buttonSair = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Sair')
                buttonSair.click()
                
                time.sleep(1)
                
                buttonSim = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Sim')
                buttonSim.click()
                
                buttonNovaNota = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Nova')
                buttonNovaNota.click()
            except: 
                buttonNovaNota = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Nova')
                buttonNovaNota.click()
                pass 
            
            print(f"Falha ao realizar emissão. {e}")
            return False
        
    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')
    
class Arrecadanet(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)
    
    def login(self, dados_adicionais = {}) -> bool:
        try:
            USUARIO_INPUT_XPATH = '//*[@id="cpf"]'
            SENHA_INPUT_XPATH = '//*[@id="senha"]'
            LOGIN_BUTTON_XPATH = '/html/body/app-root/mega-home/div/mega-login/div/div/form/div[4]/div/mega-botao/button'
            ANUNCIO_BUTTON_XPATH = '/html/body/app-root/app-boas-vindas/div/div[2]/map/area'
            NFSE_BUTTON_XPATH = '/html/body/app-root/dashboard/div/div/div/div[1]/div/mega-fieldset/div[2]/div[1]/dashboard-botao/div/div/a'
           
            inputLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            )
            inputLogin.send_keys(self.usuario)
            
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            buttonLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            time.sleep(1)
            
            try:
                buttonAnuncio = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, ANUNCIO_BUTTON_XPATH))
                )
                buttonAnuncio.click()
            except:
                pass
            
            buttonNovaNota = self.wait.until(
                EC.presence_of_element_located((By.XPATH, NFSE_BUTTON_XPATH))
            )
            buttonNovaNota.click()
            
            time.sleep(5)
            
            return True
            
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> None:
        try:
            inputCpf = self.wait.until(
                EC.presence_of_element_located((By.XPATH,  '//*[@id="cpfCnpj"]'))
            )
            inputCpf.send_keys(nota["CPF_CNPJ"])
            
            time.sleep(1)
            
            inputCpf.send_keys(Keys.TAB)
            
            time.sleep(5)
            
            try:
                buttonContinuar = self.navegador.find_element('xpath', '/html/body/ngb-modal-window/div/div/div[2]/div[2]/div/mega-table/div/table/tbody/tr/td[5]/mega-botao/button')
                buttonContinuar.send_keys(Keys.ESCAPE)
                
            except NoSuchElementException:
                pass
            
            time.sleep(1)
            
            inputNome = self.navegador.find_element('xpath', '//*[@id="nome"]')

            if(not inputNome.get_attribute('value')):
                inputNome.send_keys(nota["NOME"])

            inputLogradouro = self.navegador.find_element('xpath', '//*[@id="endereco"]')

            if(not inputLogradouro.get_attribute('value')):
                inputLogradouro.send_keys(nota["RUA"])

            inputNumero = self.navegador.find_element('xpath', '//*[@id="numero"]')

            if(not inputNumero.get_attribute('value')):
                inputNumero.send_keys(nota["NUMERO"])

            inputBairro = self.navegador.find_element('xpath', '//*[@id="bairro"]')

            if(not inputBairro.get_attribute('value')):
                inputBairro.send_keys(nota["BAIRRO"])

            inputCep = self.navegador.find_element('xpath', '//*[@id="cep"]')

            if(not inputCep.get_attribute('value')):
                inputCep.send_keys('79970000')

            inputMunicipio = self.navegador.find_element('xpath', '//*[@id="atributo"]')

            if(not inputMunicipio.get_attribute('value')):
                inputMunicipio.send_keys(dados_adicionais["municipio"])

                inputMunicipio.send_keys(Keys.ESCAPE)

                time.sleep(3)

                buttonMunicipio = self.navegador.find_element('xpath', '//*[@id="ngb-typeahead-2-0"]')
                buttonMunicipio.click()
                
            time.sleep(1)
            
            buttonEtapa1 = self.navegador.find_element('xpath', '//*[@id="formEtapa1"]/div[5]/div/mega-botao[2]/button')
            buttonEtapa1.click()
                
            time.sleep(1)

            buttonMunicipio = self.navegador.find_element('xpath', '/html/body/app-root/app-gerar-nfs-e/div/div/div[2]/div[2]/div/mega-painel-etapa/div/div[2]/div/form/div[1]/div/mega-fieldset/div[2]/div[2]/mega-municipio/div/div[1]/input[1]')
            buttonMunicipio.send_keys(dados_adicionais["municipio"])

            buttonContinuar = self.navegador.find_element('xpath', '/html/body/app-root/app-gerar-nfs-e/div/div/div[2]/div[2]/div/mega-painel-etapa/div/div[2]/div/form/div[1]/div/mega-fieldset/div[2]/div[2]/mega-municipio/div/div[1]/input[1]')
            buttonContinuar.send_keys(Keys.ESCAPE)

            time.sleep(1)

            buttonMunicipio = self.navegador.find_element('xpath', '//*[@id="ngb-typeahead-3-0"]')
            buttonMunicipio.click()

            time.sleep(1)

            inputServico = self.navegador.find_element('xpath', '//*[@id="item-de-servico-codigo"]')
            inputServico.send_keys(dados_adicionais["servico"])
            inputServico.send_keys(Keys.TAB)

            inputCnae = self.navegador.find_element('xpath', '//*[@id="cnae-codigo"]')
            inputCnae.send_keys(dados_adicionais["cnae"])
            inputCnae.send_keys(Keys.TAB)

            inputDescricao = self.navegador.find_element('xpath', '//*[@id="discriminacao"]')
            inputDescricao.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")

            inputValor = self.navegador.find_element('xpath', '//*[@id="valorDoServico"]')
            inputValor.clear()

            time.sleep(1)

            inputValor.send_keys(self.formatar_valor(nota["VALOR"]))

            buttonContinuar = self.navegador.find_element('xpath', '//*[@id="formEtapa2"]/div[5]/div/mega-botao[2]/button')
            buttonContinuar.click()

            time.sleep(1)

            buttonEmitir = self.navegador.find_element('xpath', '/html/body/app-root/app-gerar-nfs-e/div/div/div[2]/div[5]/div/mega-botao[1]/button')
            buttonEmitir.click()
            
            time.sleep(5)

            buttonEmitir = self.navegador.find_element('xpath', '/html/body/ngb-modal-window/div/div/div[1]/div[1]/div[2]/mega-botao[2]/button')
            buttonEmitir.click()

            time.sleep(5)

            buttonEmitir = self.navegador.find_element('xpath', '/html/body/ngb-modal-window/div/div/div[1]/div[1]/div[2]/mega-botao[1]/button')
            buttonEmitir.click()

            time.sleep(1)
            
            return True
        except Exception as e:
            self.navegador.get(dados_adicionais["url_emissao"])
            
            print(f"Falha ao emitir nota: {e}")
            return False
        
    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')

#
class AtendeNet(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)  
        
        self.wait = WebDriverWait(self.navegador, 15)
        
    def login(self, dados_adicionais = {}) -> bool:
        try:
            USUARIO_INPUT_XPATH = dados_adicionais["input_login"]
            SENHA_INPUT_XPATH = dados_adicionais["input_senha"]
            LOGIN_BUTTON_XPATH = dados_adicionais["button_login"]
            WEB_XPATH = '/html/body'
            MENU_PRINCIPAL_XPATH = '//*[@id="estrutura_menu_conjuntos"]/ul/li[1]'
            Y_MOV_BUTTON_MENU_FISCAL_XPATH = dados_adicionais["mov_button_menu_fiscal"]
            SUB_MENU_XPATH = '//*[@id="estrutura_menu_sistema"]/ul/li[4]/span'
            NFSE_BUTTON_XPATH = '/html/body/div[2]/main/div[2]/div[1]/section/div[2]/div/article/article/div[1]/aside[2]/div[1]/span[1]'
           
            if dados_adicionais.get('login_automatico', True):
                try:
                    webPrincipal = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, WEB_XPATH))
                    )
                    webPrincipal.send_keys(Keys.ESCAPE)
                except:
                    pass
                
                time.sleep(1)
                
                # Preenche as informações para login
                inputUsuario = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
                )
                inputUsuario.send_keys(self.usuario)
                
                inputSenha = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
                )
                inputSenha.send_keys(self.senha)
                
                time.sleep(1)
                
                buttonLogin = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
                )
                buttonLogin.click()
                
                time.sleep(1)
            else:
                print(f"Usuário: {self.usuario}")
                print(f"Senha: {self.senha}")
                input("Realize o login para continuar!")

            webPrincipal = self.wait.until(
                EC.presence_of_element_located((By.XPATH, WEB_XPATH))
            )
            webPrincipal.send_keys(Keys.ESCAPE)
            
            time.sleep(1)
            
            buttonAcesso = self.wait.until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Acessar'))
            )
            buttonAcesso.click()
            
            # Verificação de captcha
            input("Aguardando verificação de CAPTCHA. Pressione qualquer tecla para continuar...")
            
            # Alterna entre as abas
            all_windows = self.navegador.window_handles
            self.navegador.switch_to.window(all_windows[-1])
            
            time.sleep(2)
            
            buttonMenuFiscal = self.wait.until(
                EC.presence_of_element_located((By.XPATH, MENU_PRINCIPAL_XPATH))
            )
            ActionChains(self.navegador)\
                .move_to_element(buttonMenuFiscal)\
                .click()\
                .perform()

            time.sleep(1)

            ActionChains(self.navegador)\
                .move_by_offset(50, Y_MOV_BUTTON_MENU_FISCAL_XPATH)\
                .click()\
                .perform()
                
            time.sleep(3)
            
            buttonMenuEmissao = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SUB_MENU_XPATH))
            )
            ActionChains(self.navegador)\
                .move_to_element(buttonMenuEmissao)\
                .perform()

            time.sleep(1)

            ActionChains(self.navegador)\
                .move_by_offset(0, 50)\
                .click()\
                .perform()

            time.sleep(5)
            
            buttonEmitir = self.wait.until(
                EC.presence_of_element_located((By.XPATH, NFSE_BUTTON_XPATH))
            )
            buttonEmitir.click()
            
            time.sleep(3)
            
            buttonProximo = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'botao_proximo'))
            )
            buttonProximo.click()
            
            return True
            
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> None:
        try:
            try:
                time.sleep(5)
                # /html/body/div[2]/main/div[2]/div[1]/section[2]/div[2]/div/article/div/section/div[2]/article[2]/div/span[1]/fieldset/div/div[2]/span[4]/span/input[2]
                inputTomador = self.navegador.find_element('xpath', '//*[@id="conteudo_66020_141_1"]/div/section/div[2]/article[2]/div/span[1]/fieldset/div/div[2]/span[4]/span/input[2]')
                inputTomador.clear()
                
                time.sleep(1)
                
                inputTomador.send_keys(nota["CPF_CNPJ"])
                
                time.sleep(3)
                
                inputTomador.send_keys(Keys.ENTER)
                
                time.sleep(1)
                
                
                buttonProximo = self.navegador.find_element(By.NAME, 'botao_proximo')
                buttonProximo.click()
            
                time.sleep(2)
            except Exception as e:
                return False
            
            inputLocalPrestacao = self.navegador.find_element(By.NAME, 'LocalPrestacao.codigoReceita')
            inputLocalPrestacao.send_keys(dados_adicionais["localPrestacao"])
            inputLocalPrestacao.send_keys(Keys.TAB)
            
            time.sleep(2)
            
            inputServico = self.navegador.find_element(By.NAME, 'ListaServico.codigo')
            Select(inputServico).select_by_value(dados_adicionais["servico"])

            time.sleep(1)
            
            if dados_adicionais.get('quantidade', False):
                inputUnidade = self.navegador.find_element(By.NAME, 'UnidadeServico.codigo')
                Select(inputUnidade).select_by_value('2')
                
                time.sleep(2)
                
                inputUnidade = self.navegador.find_element(By.NAME, 'quantidadeUnidade')
                inputUnidade.send_keys('1')
                
                inputValor = self.navegador.find_element(By.NAME, 'valorUnidade')
                inputValor.clear()
            
                time.sleep(1)
                
                inputValor.click()
                inputValor.send_keys(nota["VALOR"])
                
                time.sleep(1)
                
            else:
                inputValor = self.navegador.find_element(By.NAME, 'valorServico')
                inputValor.clear()
            
                time.sleep(1)
                
                inputValor.send_keys(nota["VALOR"])
                
                time.sleep(1)
                
            if dados_adicionais.get("aliquota", None) is not None:
                inputAliquota = self.navegador.find_element(By.NAME, 'aliquota')
                inputAliquota.send_keys(dados_adicionais["aliquota"])
                
                time.sleep(1)
                
            # /html/body/div[2]/main/div[2]/div[1]/section[3]/div[2]/div/article/div/section/div[2]/article[3]/div/span[4]/fieldset/div/table/tbody/tr/td/div/div/table/tbody/tr[2]/td[1]/div/span[51]/span/textarea
            # /html/body/div[2]/main/div[2]/div[1]/section[2]/div[2]/div/article/div/section/div[2]/article[3]/div/span[4]/fieldset/div/table/tbody/tr/td/div/div/table/tbody/tr[2]/td[1]/div/span[51]/span/textarea
            inputDescricao = self.navegador.find_element(By.NAME, 'descricao')
            inputDescricao.send_keys(f'{nota["NFSE_ITEM_ID"]} - PAGAMENTO DE MENSALIDADE')
            
            
            time.sleep(2)
            
            buttonProximo.click()
            
            time.sleep(2)
            
            buttonProximo.click()
            
            time.sleep(2)

            buttonVisualizar = self.navegador.find_element(By.NAME, 'visualiza')
            if buttonVisualizar.is_selected():
                buttonVisualizar.click()
            
            time.sleep(1)

            buttonConfirmar = self.navegador.find_element(By.NAME, 'confirmar')
            buttonConfirmar.click()

            time.sleep(8)
            
            buttonEmitir = self.navegador.find_element('xpath', '/html/body/div[2]/main/div[2]/div[1]/section/div[2]/div/article/article/div[1]/aside[2]/div[1]/span[1]')
            buttonEmitir.click()
            
            time.sleep(5)
            
            buttonProximo = self.navegador.find_element(By.NAME, 'botao_proximo')
            buttonProximo.click()

            return True
                    
        except Exception as e:
            try:
                print(f"Falha ao emitir nota. {e}")
                
                buttonFechar = self.navegador.find_element('xpath', '/html/body/div[2]/main/div[2]/div[1]/section[2]/div[2]/header/aside/span[1]/input')
                buttonFechar.click()
                
                time.sleep(5)
                
                buttonEmitir = self.navegador.find_element('xpath', '/html/body/div[2]/main/div[2]/div[1]/section/div[2]/div/article/article/div[1]/aside[2]/div[1]/span[1]')
                buttonEmitir.click()
                
                time.sleep(5)
                
                buttonProximo = self.navegador.find_element(By.NAME, 'botao_proximo')
                buttonProximo.click()
            except:
                pass
            
            return False

#
class Ginfes(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)
    
    def login(self, dados_adicionais = {}) -> bool:
        try:
            USUARIO_INPUT_XPATH = '/html/body/div[1]/div[1]/form/div/div/div/div[1]/div[3]/input'
            SENHA_INPUT_XPATH = '/html/body/div[1]/div[1]/form/div/div/div/div[2]/div/input'
            LOGIN_BUTTON_XPATH = '/html/body/div[1]/div[1]/form/div/div/div/div[4]/div/button'
            PRESTADOR_BUTTON_XPATH = '/html/body/div[1]/div[1]/form/div/div/div/div/section/div[2]/div/div[2]/div/table/tbody/tr[3]/td[6]/button'
            
            inputLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            )
            inputLogin.send_keys(self.usuario)
            
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            time.sleep(1)
            
            buttonLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            time.sleep(1)
            
            buttonPrestador = self.wait.until(
                EC.presence_of_element_located((By.XPATH, PRESTADOR_BUTTON_XPATH))
            )
            buttonPrestador.click()
            
            time.sleep(5)
            
            self.navegador.get(dados_adicionais['url_emissao'])
            
            return True
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> None:
        try:
            time.sleep(1)    
        
            inputCpf = self.navegador.find_element('xpath', '//*[@id="buscarTomador"]')
            inputCpf.send_keys(nota["CPF_CNPJ"])
            
            time.sleep(1)
            
            buttonPesquisar = self.navegador.find_element('xpath', '/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[2]/button')
            buttonPesquisar.click()
            
            buttonAvancar = self.navegador.find_element('xpath', '//html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/fieldset[2]/div/div[1]/div[1]/div/div/div/div[1]/ul[1]/li')
            buttonAvancar.click()
            
            time.sleep(3)
            
            inputAtividade = self.navegador.find_element('xpath', '//*[@id="atividadeServico"]')
            Select(inputAtividade).select_by_value('25.01 / 9603304 - Serviços De Funerárias')
            
            time.sleep(1)
            
            inputValor = self.navegador.find_element('xpath', '//*[@id="valorServico"]')
            inputValor.send_keys(self.formatar_valor(nota["VALOR"]))
            
            # inputAtividadeCodigo = self.navegador.find_element('xpath', '/html/body/div[11]/div/div[2]')
            # inputAtividadeCodigo.click()
            
            time.sleep(1)
            
            inputDescricao = self.navegador.find_element('xpath', '//*[@id="discriminacaoServico"]')
            inputDescricao.send_keys("PAGAMENTO DE MENSALIDADE")
            
            # inputAliquota = self.navegador.find_element('xpath', '/html/body/div[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/div/div[2]/div/div[2]/div/div/div/div/div/form/fieldset[3]/div/div/div[1]/div/div/div/div[4]/div/div/div/div[1]/input')
            # inputAliquota.send_keys(dados_adicionais["aliquota"])
            
            buttonAvancar = self.navegador.find_element('xpath', '/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div[1]/form/div/div/button')
            buttonAvancar.click()
            
            time.sleep(2)
            buttonAvancar = self.navegador.find_element('xpath', '/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/div/div/button[2]')
            buttonAvancar.click()
            

            buttonEmitir = self.navegador.find_element('xpath', '/html/body/div[1]/main/div[2]/div[2]/div/div/wizard/div/div/div/div/form/div/div/button[2]')
            buttonEmitir.click()
            
            time.sleep(3)
            
            buttonAlert = self.navegador.find_element('xpath', '/html/body/div[11]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]')
            buttonAlert.click()
            
            time.sleep(1)
            
            buttonAlert = self.navegador.find_element('xpath', '/html/body/div[11]/div[2]/div[2]/div/div/div/div/div/table/tbody/tr/td[4]/table/tbody/tr/td[2]')
            buttonAlert.click()
            
            time.sleep(1)
            
            return True
        except Exception as e:
            self.navegador.refresh()            
            time.sleep(5)
            
            print(f"Falha ao emitir nota. {e}")
            return False  

    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')
    
class GovBetha(Plataforma):  
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)
    
    def login(self, dados_adicionais) -> bool:
        try:
            USUARIO_INPUT_XPATH = '//*[@id="login:iUsuarios"]'
            SENHA_INPUT_XPATH = '//*[@id="login:senha"]'
            LOGIN_BUTTON_XPATH = '//*[@id="login:btAcessar"]'
            
            inputLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            )
            inputLogin.send_keys(self.usuario)
            
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            time.sleep(1)
            
            buttonLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            time.sleep(1)
            
            # Navega até a seleção de módulos.
            self.navegador.get(dados_adicionais["url_selecao"])
            
            time.sleep(1)
            
            # Seleciona o prestador.
            buttonPrestador = self.wait.until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, dados_adicionais["cnpj"]))
            )
            buttonPrestador.click()
            
            time.sleep(1)
            
            return True
        
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> bool:
        try:
            self.navegador.get(dados_adicionais["url_emissao"])
            
            time.sleep(5)
            
            inputCpfTomador = self.navegador.find_element('xpath', '//*[@id="mainForm:inscricao"]')
            inputCpfTomador.clear()
            inputCpfTomador.send_keys(nota["CPF_CNPJ"])

            inputCpfTomador.send_keys(Keys.TAB)
            
            time.sleep(1)
            
            inputInscricaoMunicipal = self.navegador.find_element('xpath', '//*[@id="mainForm:inscricaoMunicipal"]')            
            if(not inputInscricaoMunicipal.get_attribute('value')):
                inputInscricaoMunicipal.clear()
                inputInscricaoMunicipal.send_keys('000')
                
            inputInscricaoEstadual = self.navegador.find_element('xpath', '//*[@id="mainForm:inscricaoEstadual"]')            
            if(not inputInscricaoEstadual.get_attribute('value')):
                inputInscricaoEstadual.clear()
                inputInscricaoEstadual.send_keys('000')
                
                time.sleep(1)
                
                inputInscricaoEstadual.send_keys(Keys.TAB)
                
            time.sleep(1)
                
            try:
                buttonAlterarTomador = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Alterar o registro atual')
                WebDriverWait(self.navegador, 10).until(
                    EC.element_to_be_clickable(buttonAlterarTomador)
                )       
                buttonAlterarTomador.click()
            except:
                self.navegador.find_element('xpath', '/html/body').send_keys(Keys.ESCAPE)
                
            
            inputNomeTomador = self.navegador.find_element('xpath', '//*[@id="mainForm:nome"]')            
            if(not inputNomeTomador.get_attribute('value')):
                inputNomeTomador.clear()
                inputNomeTomador.send_keys(nota["NOME"])
                
            inputCepTomador = self.navegador.find_element('xpath', '//*[@id="mainForm:cepT"]')            
            if(not inputCepTomador.get_attribute('value')):
                inputCepTomador.clear()
                inputCepTomador.send_keys(nota["CEP"])
                
            inputIdMunicipio = self.navegador.find_element('xpath', '//*[@id="mainForm:iMunicipios"]')
            if(not inputIdMunicipio.get_attribute('value')):
                inputIdMunicipio.clear()
                inputIdMunicipio.send_keys(dados_adicionais["municipio"])
                
                inputIdMunicipio.send_keys(Keys.TAB)
                
            time.sleep(3)
           
            try:
                inputCnae = self.navegador.find_element('xpath', '//*[@id="mainForm:iCnaes"]')
                inputCnae.send_keys(dados_adicionais["cnae"])
                
                inputCnae.send_keys(Keys.TAB)
            except:
                pass
            
            time.sleep(1)
            
            inputServico = self.navegador.find_element('xpath', '//*[@id="mainForm:iListaServicos"]')
            inputServico.send_keys(dados_adicionais["servico"])
            
            inputServico.send_keys(Keys.TAB)
            
            time.sleep(1)
           
            inputDescricaoServico = self.navegador.find_element('xpath', '//*[@id="mainForm:discriminacao"]')
            inputDescricaoServico.clear()
            inputDescricaoServico.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")
            
            time.sleep(2)
           
            inputValorServico = self.navegador.find_element('xpath', '//*[@id="mainForm:valorUnitario"]')
            inputValorServico.clear()
            
            time.sleep(1)
            
            inputValorServico.send_keys(self.formatar_valor(nota["VALOR"]))

            inputValorServico.send_keys(Keys.TAB)
            
            time.sleep(1)
            
            buttonAdicionarServico = self.navegador.find_element('xpath', '//*[@id="mainForm:btInsertService"]')
            telaServico = self.navegador.find_element('xpath', '//*[@id="mainForm:serv"]')
          
            self.navegador.execute_script("arguments[0].scrollIntoView();", telaServico)
            
            WebDriverWait(self.navegador, 10).until(
                EC.element_to_be_clickable(buttonAdicionarServico)
            )       
            
            buttonAdicionarServico.click()
            
            time.sleep(1)  
           
            buttonEmitir = self.navegador.find_element('xpath', '//*[@id="mainForm:btEmitir1"]') 
            buttonEmitir.click()
            
            time.sleep(5) 
            
            buttonNovaEmissao = self.navegador.find_element('xpath', '//*[@id="mainForm:btCreate"]')
            buttonNovaEmissao.click()
            
            return True
            
        except Exception as e:
            print(f"Falha ao emitir a nota. {e}")
            return False
        
    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')

#
class GovBr(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)
    
    def login(self, dados_adicionais) -> bool:
        try:
            USUARIO_INPUT_XPATH = '//*[@id="Usuario"]'
            SENHA_INPUT_XPATH = '//*[@id="Senha"]'
            LOGIN_BUTTON_XPATH = '//*[@id="Botao-Entrar"]'
            PRESTADOR_BUTTON_XPATH = dados_adicionais["prestador"]
            MENU_BUTTON_XPATH = '/html/body/div[2]/div[4]/div/ul/li[1]/a'
            
            inputLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            )
            inputLogin.send_keys(self.usuario)
            
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            time.sleep(1)
            
            buttonLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            time.sleep(5)
            
            buttonPrestador = self.wait.until(
                EC.presence_of_element_located((By.XPATH, PRESTADOR_BUTTON_XPATH))
            )
            buttonPrestador.click()
         
            time.sleep(2)
            
            buttonMenu = self.wait.until(
                EC.presence_of_element_located((By.XPATH, MENU_BUTTON_XPATH))
            )
            ActionChains(self.navegador)\
                .move_to_element(buttonMenu)\
                .perform()

            time.sleep(2)

            ActionChains(self.navegador)\
                .move_by_offset(0, 50)\
                .click()\
                .perform()
                
            return True
                
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> None:
        try:
            time.sleep(10)
            
            inputCpf = self.navegador.find_element('xpath', '//*[@id="DocumentoTomador"]')
            inputCpf.send_keys(nota["CPF_CNPJ"].replace('.', '').replace('-', ''))
            
            time.sleep(3)
            
            inputCpf.send_keys(Keys.ENTER)
            
            time.sleep(5)
            
            try:
                buttonOk = self.navegador.find_element('xpath', '//*[@id="BotaoSelecionar"]')
                buttonOk.click()
            except:
                pass

            inputServico = self.navegador.find_element('xpath', '//*[@id="Servico"]')
            inputServico.send_keys(dados_adicionais["servico"])
            
            time.sleep(3)
            
            inputServico.send_keys(Keys.ENTER)
            
            time.sleep(5)
            
            try:
                self.navegador.find_element('xpath', '/html/body/div[22]/div[2]/div/button[1]').click()
            except:
                pass
            
            time.sleep(3)
            
            inputAliquota = self.navegador.find_element('xpath', '//*[@id="ServicoViewModel_Aliquota"]')
            inputAliquota.clear()
            inputAliquota.send_keys('401')
            
            time.sleep(2)
            
            try:
                self.navegador.find_element('xpath', '/html/body/div[22]/div[2]/div/button[2]').click()
            except:
                pass
            
            time.sleep(2)
                
            inputValor = self.navegador.find_element('xpath', '//*[@id="ValorServico"]')
            inputValor.send_keys(self.formatar_valor(nota["VALOR"]))

            time.sleep(1)
            
            inputDescricao = self.navegador.find_element('xpath', '//*[@id="DescricaoServico"]')
            inputDescricao.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")

            time.sleep(3)
                    
            buttonEmitir = self.navegador.find_element('xpath', '//*[@id="gerarNotaFim"]')
            buttonEmitir.click()

            time.sleep(15)

            buttonConfirmar = self.navegador.find_element('xpath', '//*[@id="Janela-Modal"]/div/div[2]/div/div[4]/div[2]/a')
            buttonConfirmar.click()
            
            return True
        except Exception as e:            
            self.navegador.refresh()     
            print(f"Falha ao emitir nota. {e}")
            return False

    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')     

#
class GpCoplan(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)
        
    def login(self, dados_adicionais) -> bool:
        try:
            USUARIO_INPUT_XPATH = '//*[@id="vUSUARIO_LOGIN"]'
            SENHA_INPUT_XPATH = '//*[@id="vUSUARIO_SENHA"]'
            LOGIN_BUTTON_XPATH = '//*[@id="BTN_ENTER3"]'
            PRESTADOR_BUTTON_XPATH = '/html/body/form/section/table/tbody/tr[4]/td/div/div/table[1]/tbody/tr[7]/td/table/tbody/tr[1]/td/div/table/tbody/tr/td[3]/img'
            NFSE_BUTTON_XPATH = dados_adicionais["button_emissao"]
            
            inputLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            )
            inputLogin.send_keys(self.usuario)
            
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            time.sleep(1)
            
            input("Aguarde a verificação do CAPTCHA.")
            
            buttonLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            time.sleep(1)
            
            # Navega até a seleção de módulos.
            self.navegador.get(dados_adicionais["url_selecao"])
            
            time.sleep(1)
            
            # Seleciona o prestador.
            buttonPrestador = self.wait.until(
                EC.presence_of_element_located((By.XPATH, PRESTADOR_BUTTON_XPATH))
            )
            buttonPrestador.click()
            
            time.sleep(1)
            
            # Encaminha para tela de emissão.
            buttonNfse = self.wait.until(
                EC.presence_of_element_located((By.XPATH, NFSE_BUTTON_XPATH))
            )
            buttonNfse.click()
            
            return True
        
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
 
    def emitir(self, nota, dados_adicionais) -> None:
        try:
            self.navegador.refresh()
            
            time.sleep(1)
            
            CPF_INPUT_XPATH = '//*[@id="vNFSE_TOMADOR_CPF_CNPJ_MASC"]'
            DESCRICAO_INPUT_XPATH = '//*[@id="vNFSE_IPS_DISCRIMINACAO"]'
            VALOR_INPUT_XPATH = '//*[@id="vNFSE_IPS_VALOR_SERVICOS"]'
            RAZAO_INPUT_XPATH = '//*[@id="vNFSE_TOMADOR_RAZAO_SOC"]'
            ALIQUOTA_SELECT_XPATH = '//*[@id="vNFSE_IPS_LEI_COMP_ID"]'
            EMITIR_BUTTON_XPATH = '//*[@id="BTN_ENTER"]'
            ENDERECO_INPUT_XPATH = '//*[@id="vNFSE_TOMADOR_LOGRA_END"]'
            NUMERO_INPUT_XPATH = '//*[@id="vNFSE_TOMADOR_LOGRA_NUM"]'
            BAIRRO_INPUT_XPATH = '//*[@id="vNFSE_TOMADOR_LOGRA_BAIRRO"]'
            CEP_INPUT_XPATH = '//*[@id="vNFSE_TOMADOR_CEP"]'
            ESTADO_SELECT_XPATH ='//*[@id="vESTADO_ID"]'
            MUNICIPI_SELECT_XPATH = '//*[@id="vNFSE_TOMADOR_CIDADE_ID"]' 
            
            inputCpf = self.wait.until(
                EC.presence_of_element_located((By.XPATH, CPF_INPUT_XPATH))
            )
            inputCpf.send_keys(nota["CPF_CNPJ"])
            inputCpf.send_keys(Keys.TAB)
            
            time.sleep(2)

            inputRazao = self.wait.until(
                EC.presence_of_element_located((By.XPATH, RAZAO_INPUT_XPATH))
            )
            if not inputRazao.get_attribute('data-gxoldvalue'):
                time.sleep(2)
                
                inputRazao.send_keys(nota["NOME"])
                
                inputEndereco = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, ENDERECO_INPUT_XPATH))
                )
                inputEndereco.send_keys(nota["RUA"])
                            
                inputNumero = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, NUMERO_INPUT_XPATH))
                )
                inputNumero.send_keys(nota["NUMERO"])
                
                inputBairro = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, BAIRRO_INPUT_XPATH))
                )
                inputBairro.send_keys(nota["BAIRRO"])
                
                inputCep = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, CEP_INPUT_XPATH))
                )
                inputCep.send_keys(dados_adicionais["cep"])
                
                time.sleep(1)
                
                inputEstado = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, ESTADO_SELECT_XPATH))
                )
                # inputEstado.send_keys('MT')
                # inputEstado.send_keys(Keys.TAB)
                Select(inputEstado).select_by_value(dados_adicionais["estado"])
                
                time.sleep(1)
                
                inputMunicipio = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, MUNICIPI_SELECT_XPATH))
                )
                Select(inputMunicipio).select_by_value(dados_adicionais["municipio"])
                # inputMunicipio.send_keys('FELIZ NATAL')
                # inputMunicipio.send_keys(Keys.TAB)
                
            time.sleep(1)

            inputServico = self.wait.until(
                EC.presence_of_element_located((By.XPATH, ALIQUOTA_SELECT_XPATH))
            )
            Select(inputServico).select_by_value('1413')
            
            time.sleep(1)

            inputDescricao = self.wait.until(
                EC.presence_of_element_located((By.XPATH, DESCRICAO_INPUT_XPATH))
            )
            inputDescricao.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")
            
            time.sleep(1)

            inputValor = self.wait.until(
                EC.presence_of_element_located((By.XPATH, VALOR_INPUT_XPATH))
            )
            self.navegador.execute_script(f"arguments[0].value = {self.formatar_valor(nota['VALOR'])}", inputValor)
            inputValor.send_keys(Keys.TAB)

            inputValor = self.wait.until(
                EC.presence_of_element_located((By.XPATH, VALOR_INPUT_XPATH))
            )
                
            time.sleep(1)

            inputEmitir = self.wait.until(
                EC.presence_of_element_located((By.XPATH, EMITIR_BUTTON_XPATH))
            )
            inputEmitir.click()
            
            time.sleep(3)
            
            self.navegador.find_element(By.XPATH, "//*[contains(text(), 'OPERAÇÃO REALIZADA COM SUCESSO!')]")

            time.sleep(1)
            
            return True
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False

    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')
 
class IssNet(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        print("Inicie o navegador (Chrome) na opção debugger. Siga os passos:")
        print("- cd c:\\Program Files\\Google\\Chrome\\Application")
        print("- .\\chrome.exe --remote-debugging-port=9222")
        
        input("Aguardando verificação de CAPTCHA. Pressione qualquer tecla para continuar...")
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        # Inicialização do driver do Chrome
        self.navegador = webdriver.Chrome(options=chrome_options)

        # Listar as janelas abertas
        windows = self.navegador.window_handles

        # Alternar para cada janela e imprimir o título
        for window in windows:
            self.navegador.switch_to.window(window)
            
        self.wait = WebDriverWait(self.navegador, 15)
          
    def login(self, dados_adicionais = {}) -> bool:
        try:  
            input("Login")          
            # USUARIO_INPUT_XPATH = '//*[@id="txtLogin"]'
            # SENHA_INPUT_XPATH1 = f'//*[contains(@value, "{self.senha} -")]'
            # SENHA_INPUT_XPATH2 = f'//*[contains(@value, "- {self.senha}")]'
            # LOGIN_BUTTON_XPATH = '//*[@id="btnAcessar"]'
            # PRESTADOR_BUTTON_XPATH = '//*[@id="dgEmpresasNFE__ctl4_imbSelecione"]'
            
            # inputLogin = self.wait.until(
            #     EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            # )
            # inputLogin.send_keys(self.usuario)
            
            # for i in range(6):
            #     try:
            #         WebDriverWait(self.navegador, 2).until(
            #             EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH1))
            #         ).click()
            #     except:
            #         WebDriverWait(self.navegador, 2).until(
            #             EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH2))
            #         ).click()
                    
            # time.sleep(2)
            
            # buttonLogin = self.wait.until(
            #     EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            # )
            # buttonLogin.click()
            
            # time.sleep(2)
            
            # # Seleciona o prestador.
            # buttonPrestador = self.wait.until(
            #     EC.presence_of_element_located((By.XPATH, PRESTADOR_BUTTON_XPATH))
            # )
            # buttonPrestador.click()
            
            return True

        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> None:
        try:
            time.sleep(5)
            
            self.navegador.refresh()
            
            time.sleep(2)
            
            try:
                buttonEmitir = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Emitir NFS-e')
                buttonEmitir.click()

                time.sleep(1)

            except:
                buttonMenu = self.navegador.find_element('xpath', '//*[@id="menu-toggle"]')
                buttonMenu.click()
                
                time.sleep(1)
                
                buttonEmitir = self.navegador.find_element(By.PARTIAL_LINK_TEXT, 'Emitir NFS-e')
                buttonEmitir.click()
                
            time.sleep(2)
            
            self.navegador.switch_to.frame('iframe')
            
            time.sleep(2)

            inputCpf = self.navegador.find_element('xpath', '//*[@id="txtCpfCnpj"]')
            inputCpf.send_keys(nota["CPF_CNPJ"])
            inputCpf.send_keys(Keys.TAB)
            
            time.sleep(2)
            
            inputCep = self.navegador.find_element('xpath', '//*[@id="txtCep"]')
            if not inputCep.get_attribute('value'):
                inputCep.send_keys(nota["CEP"])
                inputCep.send_keys(Keys.TAB)
            
            while True:
                try:
                    WebDriverWait(self.navegador, 10).until(EC.alert_is_present())
                    alert = self.navegador.switch_to.alert
                    alert.dismiss()
                    break
                except Exception as e:
                    break
                
            
            time.sleep(1)
            
            inputDescricao = self.navegador.find_element('xpath', '//*[@id="txtDescServicos"]')
            inputDescricao.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")
            
            inputAtividade = self.navegador.find_element('xpath', '//*[@id="ddllistaitemservico"]')
            Select(inputAtividade).select_by_value('2501')
            
            time.sleep(2)
            
            inputAtividadeMunicipio = self.navegador.find_element('xpath', ' //*[@id="ddlAtividade"]')
            Select(inputAtividadeMunicipio).select_by_value('15295')
           
            time.sleep(2)
            
            inputAliquota = self.navegador.find_element('xpath', '//*[@id="txtAliq"]')
            inputAliquota.send_keys(dados_adicionais["aliquota"])
            
            time.sleep(1)
            
            inputValor = self.navegador.find_element('xpath', '//*[@id="txtTotal"]')
            
            self.navegador.execute_script(f"arguments[0].value = {self.formatar_valor(nota['VALOR'])}", inputValor)
            
            inputValor.send_keys(Keys.TAB)
            
            time.sleep(1)
            
            buttonAssinar = self.navegador.find_element('xpath', '//*[@id="btnAssinar"]')
            self.navegador.execute_script("arguments[0].scrollIntoView();", buttonAssinar)
            
            time.sleep(1)
            
            buttonAssinar.click()
            
            time.sleep(3)
            
            buttonSenha = self.navegador.find_element('xpath', '//*[@id="btnAssinaSenha"]')
            buttonSenha.click()
            
            time.sleep(1)
            
            inputSenha = self.navegador.find_element('xpath', '//*[@id="txtSenhaAssinatura"]')
            for i in range(6):
               inputSenha.send_keys(self.senha)
               
            time.sleep(1)
            
            buttonOk = self.navegador.find_element('xpath', '//*[@id="btnOkAssinaSenha"]')
            buttonOk.click()
            
            return True
        except Exception as e:
            print(f"Falha ao emitir nota. {e}")
            return False

    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')
    
class IssWeb(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)

    def login(self, dados_adicionais = {}) -> bool:
        try:
            # Constantes para XPaths
            USERNAME_INPUT_XPATH = '//*[@id="username"]'
            PASSWORD_INPUT_XPATH = '//*[@id="password"]'
            LOGIN_BUTTON_XPATH = '/html/body/div[1]/div/div[1]/div/div/div/div/div[1]/div/div/form/div[4]/div/input'
            MENU_BUTTON_XPATH = '//*[@id="navNfse"]/a'
            EMITIR_BUTTON_XPATH = '/html/body/section/div/aside/div[2]/div[1]/nav/form/ul/li[3]/ul/li[1]/a'
            
            # Esperar que o campo de usuário esteja presente e enviar o usuário
            inputUsuario = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USERNAME_INPUT_XPATH))
            )
            inputUsuario.send_keys(self.usuario)
            
            # Esperar que o campo de senha esteja presente e enviar a senha
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            # Esperar que o botão de login esteja presente e clicar
            buttonLogin = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            # Esperar que o menu esteja presente e clicar
            buttonMenu = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, MENU_BUTTON_XPATH))
            )
            buttonMenu.click()
            
            # Esperar que o botão emitir esteja presente e clicar
            buttonEmitir = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, EMITIR_BUTTON_XPATH))
            )
            buttonEmitir.click()
            
            return True
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> bool:
        try:
            self.navegador.get(dados_adicionais["url_emissao"])
            
            # Constantes para XPaths
            XPATHS = {
                'tipo_emissao': '//*[@id="formEmissaoNFConvencional:tipoPessoa_input"]',
                'cpf': '//*[@id="formEmissaoNFConvencional:itCpf"]',
                'nome': '//*[@id="formEmissaoNFConvencional:razaoNome"]',
                'cep': '//*[@id="formEmissaoNFConvencional:cep"]',
                'logradouro': '//*[@id="formEmissaoNFConvencional:logradouro"]',
                'numero': '//*[@id="formEmissaoNFConvencional:numero"]',
                'bairro': '//*[@id="formEmissaoNFConvencional:bairro"]',
                'municipio': '//*[@id="formEmissaoNFConvencional:municipios_input"]',
                'cnae': '//*[@id="formEmissaoNFConvencional:listaAtvCnae_input"]',
                'atividade': '//*[@id="formEmissaoNFConvencional:listaAtvAtd_input"]',
                'aliquota': '//*[@id="formEmissaoNFConvencional:aliquotaItemNota_input"]',
                'descricao_item': '//*[@id="formEmissaoNFConvencional:descricaoItem"]',
                'valor': '//*[@id="formEmissaoNFConvencional:vlrUnitario_input"]',
                'add_item_button': '//*[@id="formEmissaoNFConvencional:btnAddItem"]',
                'emitir_button': '//*[@id="frmActions:btnDefault"]',
                'confirm_emitir_button': '//*[@id="frmActions:j_idt480"]',
                'novo_button': '//*[@id="formEmissaoNFConvencional:j_idt779"]',
                # 'inscricao_municipal': '//*[@id="formEmissaoNFConvencional:j_idt526"]'
                'inscricao_municipal': '//*[@id="formEmissaoNFConvencional:j_idt530"]'
            }

            wait = WebDriverWait(self.navegador, 10)

            # Seleciona tipo de emissão
            inputTipoEmissao = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['tipo_emissao'])))
            Select(inputTipoEmissao).select_by_value('FISICA')

            # Insere CPF
            inputCpf = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['cpf'])))
            inputCpf.click()
            inputCpf.send_keys(nota["CPF_CNPJ"])
            inputCpf.send_keys(Keys.TAB)
            
            time.sleep(3)
            
            # Insere nome se necessário
            while True:
                try:
                    inputNome = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['nome'])))
                    if not inputNome.get_attribute('value'):
                        self.navegador.execute_script(f"arguments[0].value = '{nota['NOME']}'", inputNome)
                    break
                except StaleElementReferenceException:
                    continue
        
            inputInscricao = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['inscricao_municipal'])))
            self.navegador.execute_script(f"arguments[0].value = '000'", inputInscricao)
            
            # Insere CEP
            inputCep = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['cep'])))
            self.navegador.execute_script(f"arguments[0].value = '{dados_adicionais['cep']}'", inputCep)
            
            # Insere logradouro se necessário
            while True:
                try:
                    inputLogradouro = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['logradouro'])))
                    if not inputLogradouro.get_attribute('value'):
                        self.navegador.execute_script(f"arguments[0].value = {nota['RUA']}", inputLogradouro)
                    break
                except StaleElementReferenceException:
                    continue

            # Insere número se necessário
            while True:
                try:
                    inputNumero = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['numero'])))
                    if not inputNumero.get_attribute('value'):
                        self.navegador.execute_script(f"arguments[0].value = {nota.get('NUMERO', '0')}", inputNumero)
                    break
                except StaleElementReferenceException:
                    continue

            # Insere bairro se necessário
            while True:
                try:
                    inputBairro = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['bairro'])))
                    if not inputBairro.get_attribute('value'):
                        self.navegador.execute_script(f"arguments[0].value = {nota['BAIRRO']}", inputBairro)
                    break
                except StaleElementReferenceException:
                    continue
            
            # Insere município
            while True:
                try:
                    inputMunicipio = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['municipio'])))
                    inputMunicipio.clear()
                    
                    time.sleep(2)
                    inputMunicipio.send_keys(dados_adicionais["municipio"])
                    
                    time.sleep(2)
                    inputMunicipio.send_keys(Keys.ENTER)
                    break
                except StaleElementReferenceException:
                    continue
            
            time.sleep(2)
            
            # Seleciona cnae
            while True:
                try:
                    inputCnae = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['cnae'])))
                    Select(inputCnae).select_by_value(dados_adicionais["cnae"])
                    break
                except StaleElementReferenceException:
                    continue
            
            time.sleep(2)
            
            # Seleciona atividade
            while True:
                try:
                    inputAtividade = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['atividade'])))
                    Select(inputAtividade).select_by_value(dados_adicionais["atividade"])
                    break
                except StaleElementReferenceException:
                    continue
                
            time.sleep(1)
            
            # Seleciona atividade
            if dados_adicionais.get('aliquota', None) is not None:
                while True:
                    try:
                        inputAliquota = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['aliquota'])))
                        inputAliquota.send_keys(dados_adicionais["aliquota"])
                        self.navegador.find_element('xpath', '/html/body').send_keys(Keys.ENTER)
                        break
                    except StaleElementReferenceException:
                        continue
            
            time.sleep(1)
            
            # Insere descrição do item
            inputDescricao = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['descricao_item'])))
            self.navegador.execute_script("arguments[0].value = arguments[1];", inputDescricao, f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")
            
            time.sleep(3)
            
            # Insere valor
            inputValor = wait.until(EC.presence_of_element_located((By.XPATH, XPATHS['valor'])))
            self.navegador.execute_script("arguments[0].click();", inputValor)
            inputValor.clear()
            time.sleep(2)
            inputValor.send_keys(self.formatar_valor(nota["VALOR"]))
            inputValor.send_keys(Keys.ESCAPE)

            # Adiciona item
            buttonItem = wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS['add_item_button'])))
            self.navegador.execute_script("arguments[0].click();", buttonItem)
            
            time.sleep(1.5)
            
            # Emite a nota
            buttonEmitir = wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS['emitir_button'])))
            self.navegador.execute_script("arguments[0].click();", buttonEmitir)
            
            time.sleep(1.5)
            
            # Confirma a emissão
            buttonEmitirConfirma = wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS['confirm_emitir_button'])))
            buttonEmitirConfirma.click()
            
            time.sleep(1.5)
            
            # Aguarda a finalização e tenta emitir uma nova nota
            try:
                buttonNovo = WebDriverWait(self.navegador, 10).until(
                    EC.element_to_be_clickable((By.XPATH, XPATHS['novo_button']))
                )
                buttonNovo.click()
                return True
            except NoSuchElementException as er:
                print(f"Falha ao emitir nota: {nota['NFSE_ITEM_ID']} - {nota['CPF_CNPJ']}.\nErro: {er}")
                return False
        except Exception as e:
            print(f"Falha ao emitir nota: {nota['NFSE_ITEM_ID']} - {nota['CPF_CNPJ']}.\nErro: {e}")
            return False

    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')

#    
class Nirj(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)
        
        self.wait = WebDriverWait(self.navegador, 15)
        
    def login(self, dados_adicionais = {}) -> bool:
        try:                  
            ACESSO_BUTTON_XPATH = '//*[@id="coluna1"]/div/div[2]/ul/li[2]/a'
            USUARIO_INPUT_XPATH = '//*[@id="rLogin"]'
            SENHA_INPUT_XPATH = '//*[@id="rSenha"]'
            LOGIN_BUTTON_XPATH = '//*[@id="btnEntrar"]'
            PRESTADOR_BUTTON_XPATH = '/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div[4]/ul/li/a'
            NFSE_BUTTON_XPATH = '/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div[7]/ul/li/a'
            
            frame = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'principal'))
            )
            self.navegador.switch_to.frame(frame)
            
            buttonAcesso = self.wait.until(
                EC.presence_of_element_located((By.XPATH, ACESSO_BUTTON_XPATH))
            )
            buttonAcesso.click()

            time.sleep(1)
            
            inputUsuario = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USUARIO_INPUT_XPATH))
            )
            inputUsuario.send_keys(self.usuario)
            
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, SENHA_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            # Verificação de captcha
            input("Aguardando verificação de CAPTCHA. Pressione qualquer tecla para continuar...")
            
            buttonLogin = self.wait.until(
                EC.presence_of_element_located((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            time.sleep(10)
            
            buttonPrestador = self.wait.until(
                EC.presence_of_element_located((By.XPATH, PRESTADOR_BUTTON_XPATH))
            )
            buttonPrestador.click()
            
            time.sleep(10)
            
            buttonEmitir = self.wait.until(
                EC.presence_of_element_located((By.XPATH, NFSE_BUTTON_XPATH))
            )
            buttonEmitir.click()
            
            return True
        
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
    
    def emitir(self, nota, dados_adicionais) -> None:
        try:
            time.sleep(10)
            
            inputCpf = self.navegador.find_element('xpath', '//*[@id="rTomCpfCnpjSel"]')
            inputCpf.send_keys(nota["CPF_CNPJ"])
                    
            time.sleep(4)
            
            inputCpf.send_keys(Keys.TAB)
            
            time.sleep(5)
                        
            buttonAvancar = self.navegador.find_element('xpath', '//*[@id="btnAvancar"]')  
            
            # Use execute_script para rolar até o botão Avançar
            self.navegador.execute_script("arguments[0].scrollIntoView();", buttonAvancar)

            time.sleep(3)
          
            buttonAvancar.click()
            
            time.sleep(4)
            
            inputAtividade = self.navegador.find_element('xpath', '//*[@id="rCodAtv"]')
            Select(inputAtividade).select_by_value(dados_adicionais["atividade"])
            
            time.sleep(7)
            
            buttonAvancar = self.navegador.find_element('xpath', '//*[@id="btnAvancar"]')  
            buttonAvancar.click()
            
            time.sleep(5)
            
            inputDescricao = self.navegador.find_element('xpath', '//*[@id="rDescrNota"]')
            inputDescricao.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")
            
            inputItem = self.navegador.find_element('xpath', '//*[@id="rItemDescricao"]')
            inputItem.send_keys(f"{nota['NFSE_ITEM_ID']} - PAGAMENTO DE MENSALIDADE")
            
            inputQuantidade = self.navegador.find_element('xpath', '//*[@id="rItemQtd"]')
            inputQuantidade.send_keys(1)
            
            inputValor = self.navegador.find_element('xpath', '//*[@id="rItemValUnit"]')
            inputValor.send_keys(self.formatar_valor(nota["VALOR"]))
            
            time.sleep(3)
            
            inputValor.send_keys(Keys.TAB)

            time.sleep(7)
            
            buttonEmitirNota = self.navegador.find_element('xpath', '//*[@id="btnEmitir"]')
            buttonEmitirNota.click()
            
            time.sleep(7)
            
            # Aceitar o alerta
            alert = self.navegador.switch_to.alert
            alert.accept()
            
            time.sleep(8)
            
            buttonEmitir = self.navegador.find_element('xpath', '/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div[7]/ul/li/a')
            buttonEmitir.click()
                        
            return True
        except Exception as e:
            buttonEmitir = self.navegador.find_element('xpath', '/html/body/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/div[7]/ul/li/a')
            buttonEmitir.click()
            
            print(f"Falha ao emitir nota. {e}")
            return False
        
    def formatar_valor(self, valor):
        novoValor = f"{float(valor):.2f}"
        return novoValor.replace('.', ',')

#
class Oxy(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)

        self.wait = WebDriverWait(self.navegador, 15)
        
    def login(self, dados_adicionais = {}) -> bool:
        try:
            # Constantes para XPaths
            USERNAME_INPUT_XPATH = '/html/body/app-root/div/app-theme1/app-main/main-section/section/div[1]/ng-component/user-authentication/section/div/div/div/div/form/div/input[1]'
            PASSWORD_INPUT_XPATH = '//*[@id="password"]'
            LOGIN_BUTTON_XPATH = '//*[@id="btn-login"]'
            ANUNCIO_BUTTON_XPATH = '//*[@id="btOk"]'
            
            try:
                # Esperar que o campo de usuário esteja presente e enviar o usuário
                html = WebDriverWait(self.navegador, 5).until(
                    EC.presence_of_element_located((By.XPATH, ANUNCIO_BUTTON_XPATH))
                )
                html.click()
            except:
                pass 
               
            time.sleep(2)
            
            # Esperar que o campo de usuário esteja presente e enviar o usuário
            inputUsuario = self.wait.until(
                EC.presence_of_element_located((By.XPATH, USERNAME_INPUT_XPATH))
            )
            inputUsuario.send_keys(self.usuario)
            
            # Esperar que o campo de senha esteja presente e enviar a senha
            inputSenha = self.wait.until(
                EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            time.sleep(1)
            
            # Esperar que o botão de login esteja presente e clicar
            buttonLogin = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()
            
            time.sleep(1)
            
            self.navegador.get(dados_adicionais["url_emissao"])
            
            input("Selecione o prestador dos serviços!")
            
            return True
        except NoSuchElementException:
            # Capture a exceção de elemento não encontrado e exiba uma mensagem de erro amigável
            print("Elemento não encontrado.")
            return False

        except TimeoutException:
            # Capture a exceção de tempo limite e exiba uma mensagem de erro amigável
            print("Tempo limite ao tentar encontrar o elemento.")
            return False

        except ElementNotInteractableException:
            # Capture a exceção de interação com algum elemento
            print("Erro na interação com o elemento.")
            return False

        except WebDriverException as e:
            # Capture outras exceções relacionadas ao WebDriver e exiba uma mensagem de erro amigável
            print("Erro durante a navegação ou interação com o WebDriver.")
            print(e)
            return False

        except Exception as e:
            # Capture qualquer outra exceção genérica e exiba uma mensagem de erro amigável
            print(f"Ocorreu um erro inesperado. {e}")
            return False
           
    def emitir(self) -> None:
        pass

class Quality(Plataforma):
    def __init__(self, url:str, usuario:str, senha:str):
        super().__init__(url, usuario, senha)
        
        self.navegador = webdriver.Edge()
        self.navegador.maximize_window()
        
        self.navegador.get(self.url)

    def login(self, dados_adicionais) -> bool:
        try:
            # Constantes para XPaths
            USERNAME_XPATH = '//*[@id="campoLoginLogin"]'
            PASSWORD_XPATH = '//*[@id="campoSenhaLogin"]'
            LOGIN_BUTTON_XPATH = '//*[@id="formLogin"]/a[2]'
            
            # Esperar que o campo de usuário esteja presente e enviar o usuário
            inputUsuario = WebDriverWait(self.navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, USERNAME_XPATH))
            )
            inputUsuario.send_keys(self.usuario)
            
            # Esperar que o campo de senha esteja presente e enviar a senha
            inputSenha = WebDriverWait(self.navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, PASSWORD_XPATH))
            )
            inputSenha.send_keys(self.senha)
            
            # Esperar que o botão de login esteja presente e clicar
            buttonLogin = WebDriverWait(self.navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))
            )
            buttonLogin.click()

            return True            
        except Exception as e:
            print(f"Falha ao realizar o login na plataforma. {e}")
            return False

    def emitir(self, nota, dados_adicionais) -> bool:
        try:
            # Cadastrar o tomador
            if not self.cadastrar_tomador(nota, dados_adicionais):
                return False

            # Navegar para a página de emissão
            self.navegador.get(dados_adicionais["url_emissao"])
            time.sleep(2)
            
            # Preencher os campos necessários
            self.preencher_campos_emissao(nota)
            
            time.sleep(2)
            
            # Emitir a nota
            if self.confirmar_emissao():
                print(f"Nota emitida com sucesso: {nota['NFSE_ITEM_ID']} - {nota['CPF_CNPJ']}")
                return True
            else:
                print(f"Falha ao emitir a nota: {nota['NFSE_ITEM_ID']} - {nota['CPF_CNPJ']}")
                return False
        except Exception as e:
            print(f"Falha ao emitir a nota: {nota['NFSE_ITEM_ID']} - {nota['CPF_CNPJ']}. Erro: {e}")
            return False

    def cadastrar_tomador(self, nota, dados_adicionais) -> bool:
        try:
            self.navegador.get(dados_adicionais["url_tomador"])
            time.sleep(1)
            
            # Selecionar tipo de pessoa
            checkPessoa = self.navegador.find_element(By.XPATH, '//*[@id="pess1Label"]')
            checkPessoa.click()
            time.sleep(1)
            
            # Preencher CPF e verificar se já está cadastrado
            inputCpf = self.navegador.find_element(By.XPATH, '//*[@id="campoCPF"]')
            inputCpf.send_keys(nota["CPF_CNPJ"])
            inputCpf.send_keys(Keys.TAB)
            time.sleep(3)
            
            # Verificar se tomador já está cadastrado
            if self.verificar_tomador_incluido():
                return True

            # Preencher dados do tomador
            self.preencher_dados_tomador(nota, dados_adicionais)
            return True
        except Exception as e:
            print(f"Falha ao cadastrar tomador. Erro: {e}")
            return False

    def verificar_tomador_incluido(self) -> bool:
        try:
            divAlert = self.navegador.find_element(By.XPATH, '//*[@id="boxTextoAviso"]/span')
            return 'incluído' in divAlert.text
        except NoSuchElementException:
            return False

    def preencher_dados_tomador(self, nota, dados_adicionais):
        try:
            # Preencher campos obrigatórios
            self.preencher_campo(By.XPATH, '//*[@id="campoNome"]', nota["NOME"])
            self.preencher_campo(By.XPATH, '//*[@id="campoCEP"]', dados_adicionais["cep"])
            time.sleep(1)

            # Selecionar tipo de logradouro
            self.selecionar_opcao_div((By.XPATH, '//*[@id="DivClasseTipoLog"]'), By.CLASS_NAME, 'optCb_tipoLog33')

            # Preencher logradouro, bairro
            self.preencher_campo(By.XPATH, '//*[@id="campoRua"]', nota["RUA"])
            self.preencher_campo(By.XPATH, '//*[@id="campoBairro"]', nota["BAIRRO"])

            # Selecionar estado e município
            self.selecionar_opcao_div((By.XPATH, '//*[@id="DivClasseEstado"]'), By.CLASS_NAME, 'optCb_estado_50')
            self.selecionar_opcao_div((By.XPATH, '//*[@id="DivClasseCidade"]'), By.CLASS_NAME, 'optCb_cidade5000906')

            # Preencher email
            self.preencher_campo(By.XPATH, '//*[@id="campoEmail"]', dados_adicionais["email"])
            
            # Preencher número
            self.preencher_campo(By.XPATH, '//*[@id="campoNumero"]', nota["NUMERO"])

            # Enviar formulário
            buttonEnviar = self.navegador.find_element(By.XPATH, '//*[@id="dirPrincipal"]/a')
            buttonEnviar.click()
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao preencher dados do tomador: {e}")

    def preencher_campos_emissao(self, nota):
        try:
            # Preencher campos de emissão
            self.preencher_campo(By.XPATH, '//*[@id="DivClasseTomador"]/span/input', nota["CPF_CNPJ"][:10], Keys.ARROW_DOWN, Keys.ENTER)
            self.selecionar_opcao((By.XPATH, '//*[@id="selectItensServico"]'), '204')
            self.preencher_campo(By.XPATH, '//*[@id="campoDescr"]', 'Pagamento de mensalidade')
            self.preencher_campo(By.XPATH, '//*[@id="descricaoItem_1"]', 'Pagamento de mensalidade')
            self.preencher_campo(By.XPATH, '//*[@id="valorUnitItem_1"]', self.formatar_valor(nota["VALOR"]), Keys.TAB)
        except Exception as e:
            print(f"Erro ao preencher campos de emissão: {e}")

    def confirmar_emissao(self) -> bool:
        try:
            buttonEmitir = self.navegador.find_element(By.XPATH, '//*[@id="emitirNotaBotoes"]/a[1]')
            buttonEmitir.click()
            time.sleep(1)
            buttonConfirmar = WebDriverWait(self.navegador, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="boxBot"]/a[1]'))
            )
            buttonConfirmar.click()
            time.sleep(5)
            return True
        except Exception as e:
            print(f"Erro ao confirmar emissão: {e}")
            return False

    def preencher_campo(self, by, locator, valor, *keys):
        inputElement = WebDriverWait(self.navegador, 10).until(
            EC.presence_of_element_located((by, locator))
        )
        inputElement.clear()
        inputElement.send_keys(valor)
        for key in keys:
            inputElement.send_keys(key)

    def selecionar_opcao(self, by_locator, option_locator):
        try:
            inputElement = WebDriverWait(self.navegador, 10).until(EC.presence_of_element_located(by_locator))
            Select(inputElement).select_by_value(option_locator)
        except Exception as e:
            print(f"Erro ao selecionar a opção {option_locator} para {by_locator}. Erro: {e}")
    
    def selecionar_opcao_div(self, by_locator, option_by, option_locator):
        while True:
            try:
                element = WebDriverWait(self.navegador, 10).until(
                    EC.presence_of_element_located(by_locator)
                )
                self.navegador.execute_script("arguments[0].scrollIntoView(true);", element)
                self.navegador.execute_script("arguments[0].click();", element)
                
                option = WebDriverWait(self.navegador, 10).until(
                    EC.presence_of_element_located((option_by, option_locator))
                )
                self.navegador.execute_script("arguments[0].scrollIntoView(true);", option)
                self.navegador.execute_script("arguments[0].click();", option)
                
                break
            except StaleElementReferenceException:
                continue
            except Exception as e:
                print(f"Erro ao selecionar a opção {option_locator} para {by_locator}. Erro: {e}")
                break
            
    def formatar_valor(self, valor):
        return f"{valor:.2f}"