from database import Database
from validate_docbr import CPF
import plataformas
import firebirdsql
import json

class EmissaoNotas:
    db = None
    cursor = None
    classe = None
    valorEmitido: float = 0
    validate_cpf = CPF()
    
    def __init__(self):
        try:
            print("Iniciando processamento!")
            with open("conexao.json", encoding='utf-8') as file:
                data = json.load(file)
            
            # Exibir lista de unidades para seleção
            print("Selecione a unidade para emitir:")
            unidades_ativas = [unidade for unidade in data if unidade["status"]]
            for i, unidade in enumerate(unidades_ativas):
                print(f"{i + 1}. {unidade['nome']}")

            while True:
                try:
                    escolha = int(input("Digite o número da unidade desejada: ")) - 1
                    if escolha < 0 or escolha >= len(unidades_ativas):
                        print("Opção inválida. Por favor, escolha um número válido.")
                    else:
                        unidade = unidades_ativas[escolha]
                        print("___________________________________________________________________________")
                        print(f"Acessando unidade {unidade['nome']}")
                                
                        self.classe = getattr(plataformas, unidade["class"])
                        if not (hasattr(self.classe, "login") and callable(getattr(self.classe, "login"))):
                            print(f"Classe {unidade['class']} não definida!")
                            return
                        
                        try:
                            self.conectar(unidade)
                            print("Conexão realizada com sucesso!")
                            
                            clientes = self.buscarClientes()
                            
                            notas = self.processarClientes(unidade, clientes)
                            
                            if len(notas)>0:
                                self.processarNotas(unidade, notas)

                            self.db.close_cursor()
                            self.db.close_connection()   
                              
                            print(f"Finalizado o processamento de notas de {unidade['nome']}. Valor emitido: {self.valorEmitido}")
                            print("___________________________________________________________________________")  
                                                       
                            unidades_ativas.pop(escolha)
                            if not unidades_ativas:
                                print("Todas as unidades foram processadas.")
                                break
                            else:
                                print("Selecione outra unidade para continuar o processamento:")
                                for i, unidade in enumerate(unidades_ativas):
                                    print(f"{i + 1}. {unidade['nome']}")     
                        except Exception as e: 
                            print(f"Falha ao processar as notas da unidade {unidade['nome']}. {e}")
                            return
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")                    
        except Exception as e:
            print(f"Ocorreu um erro. {e}")
        finally:              
            print("Fim processamento")
            
    def conectar(self, unidade):
        self.db = Database(
            host=unidade["db_host"], 
            database=unidade["db_database"],
            usuario=unidade["db_user"],
            
            senha=unidade["db_password"],
            port=unidade["db_port"]
        )
            
        self.db.connect_to_db()
        self.cursor = self.db.get_db_cursor()
            
    def buscarClientes(self): 
        try:
            self.cursor.execute(
            f"""
                select
                    ni.nfse_item_id, ni.data_cadastro, c.cpf_cnpj, c.nome, c.cep as cep, c.rua as logradouro, 
                    case when c.numero is null or c.numero='' then '0' else c.numero end as numero, b.descricao as bairro, ni.valor, 0 as status
                from nfse_item ni 
                left join nfse_cliente nc on nc.nfse_cliente_id = ni.nfse_cliente_id
                left join cliente c on c.idcliente = nc.cliente_id
                left join bairro b on b.id = c.bairro_cob
                where ni.nfse_item_id in (68787, 68900, 69807, 68737, 69737, 69714, 69013, 69359, 68696, 69012, 68919, 69656, 69437, 69134, 69294, 69486, 68793, 69257, 68950, 69347, 69694, 68746, 69672, 69853, 69477, 69678, 69223, 69762, 69355, 69798, 69098, 69788, 69592, 69409, 69047, 68761, 69057, 69414, 69729, 69651, 69380, 69501, 69379)                                
            """)
            
            
            #                             56274, 56107, 56158, 56614, 56161, 56318, 56506, 56526, 56119, 56259, 56265, 56330, 56572, 56583, 56209, 56421, 56270, 56006, 56602, 56527, 56370, 56610, 56547, 56053, 56424, 56061, 56217, 56282, 56233, 56159, 56190, 56367, 56423, 56576, 56501, 56606, 56677, 56429, 56316, 56331, 56197, 56176, 56522
            #  ni.data_cadastro between
            #         cast(dateadd(day, -extract(day from current_date) + 1, current_date) as date) 
            #         and 
            #         cast(dateadd(month, 1, dateadd(day, -extract(day from current_date), current_date)) as date)
            #     order by ni.valor desc, ni.nfse_item_id desc
            
            return self.cursor.fetchall()
        
        except firebirdsql.OperationalError as e:
            raise Exception(f"Falha ao realizar consulta: {e}")
        
    def processarNotas(self, unidade, notas):
        classeNotas = self.classe(
            url=unidade["url_portal"], 
            usuario=unidade["usuario_portal"], 
            senha=unidade["senha_portal"]
        )
        
        
        print(notas)
        dados_adicionais = unidade.get("dados_adicionais", {})
        login = classeNotas.login(dados_adicionais=dados_adicionais)
        if not login:
            return
          
        for nota in notas:
            if self.valorEmitido > unidade["limite"]:
                print("Valor teto atingido!")
                break
            
            result = classeNotas.emitir(nota, dados_adicionais)
            print(result)
            print(nota)
            if result:
                self.valorEmitido += nota["VALOR"]
                self.atualizarNotas(nota["NFSE_ITEM_ID"], 1)
            else:
                self.atualizarNotas(nota["NFSE_ITEM_ID"], 0)
                
    def atualizarNotas(self, nota, status):
        try:
            if(nota):
                self.cursor.execute(
                f"""
                    update nfse_item set status={status} where nfse_item_id = {nota};                        
                """
                )

                self.db.commit()
                
                if status == 1:
                    print(f"Valor emitido: {float(self.valorEmitido):.2f}")
            
        except Exception as e:
            print(f"Falha ao realizar consulta: {e}")
     
    def processarClientes(self, unidade, clientes):
        limite = 0
        notasPendentes = []
        valorEmitido = 0
        valorPendente = 0
        
        while True:
            try:
                unidade["limite"] = limite = float(input("Informe o valor teto: "))
                break
            except ValueError:
                print("Valor inválido.")
        
        for c in clientes:
            cliente = {
                "NFSE_ITEM_ID": c[0],
                "CPF_CNPJ": CPF().mask(str(c[2]).replace('.', '').replace('-', '')),
                "NOME": c[3],
                "CEP": c[4] if c[4] is not None and c[4] != '' else unidade["dados_adicionais"].get("cep", ""),
                "RUA": c[5],
                "NUMERO": c[6] if c[6] is not None and c[6] != '' else '0',
                "BAIRRO": c[7],
                "VALOR": float(c[8]),
                "STATUS": c[9]
            }
            
            if cliente["STATUS"] == '1':
                valorEmitido += float(c[8])
            elif cliente["STATUS"] != '2' and self.validate_cpf.validate(cliente["CPF_CNPJ"]):
                valorPendente += float(c[8])
                notasPendentes.append(cliente)
            elif cliente["STATUS"] != '2':
                self.atualizarNotas(cliente["NFSE_ITEM_ID"], 2)
                
        self.valorEmitido = valorEmitido
        print(f"Valor pendente: {float(valorPendente):.2f}")
        print(f"Valor emitido: {float(valorEmitido):.2f}")
        print(f"Valor teto: {limite}")
        
        if valorEmitido >= limite:
            print("Valor teto atingido!")
            resposta = input("Deseja continuar emitindo acima do teto? (s/n): ")
            if resposta.lower() == 's':
                try:
                    novo_limite = float(input("Informe o novo valor teto temporário: "))
                    unidade["limite"] = novo_limite
                except ValueError:
                    print("Valor inválido. Finalizando o programa.")
                    return []
            else:
                return []
            
        return notasPendentes
 
EmissaoNotas()