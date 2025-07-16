from firebird.driver import Connection
from datetime import date
def get_nfse_cliente(con: Connection, dataInicial : date, dataFinal: date) -> list[tuple]:
    
        cursor_db = con.cursor()

        query = "SELECT n.nfse_item_id, n.data_cadastro, n.valor, n.status, c.cpf_cnpj, c.nome " +\
                "FROM nfse_item n JOIN cliente c on n.nfse_cliente_id = c.idcliente " +\
                f"WHERE n.data_cadastro BETWEEN ? AND ?;"
        
        cursor_db.execute(query, (dataInicial, dataFinal))

        return cursor_db.fetchall()