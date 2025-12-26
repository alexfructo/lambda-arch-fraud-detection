import mysql.connector
import logging

logger = logging.getLogger("mysql-client")

def create_mysql_connection(
    host: str,
    database: str,
    user: str,
    password: str
):
    """
    Cria e retorna uma conexão MySQL.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            autocommit=True
        )
        logger.info("Conexão com MySQL estabelecida com sucesso")
        return conn

    except mysql.connector.Error as e:
        logger.exception("Erro ao conectar no MySQL")
        raise e
