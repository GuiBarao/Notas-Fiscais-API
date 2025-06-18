from firebird.driver import Connection

def get_nfse_cliente(con: Connection) -> list[tuple]:
    
        cursor_db = con.cursor()

        query = "SELECT nfse_item_id, data_cadastro, valor, status , mensagem , log, cpf_cnpj, nome " +\
                "FROM nfse_item, cliente " +\
                "WHERE nfse_cliente_id = idcliente;"
        
        cursor_db.execute(query)

        return cursor_db.fetchall()