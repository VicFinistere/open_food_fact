import pymysql


class Connection:
    @staticmethod
    def connect_to_database():
        connection = pymysql.connect(host="127.0.0.1",  # The Host
                                     user="root",  # username
                                     passwd="P0rt1she@d",  # password
                                     db="openfoodfact",
                                     port=3306)  # name of the data base

        cursor = connection.cursor()
        # print("Connexion")
        return connection, cursor

    @staticmethod
    def close_database_connection(cursor, connection):
        # MySQL connection
        cursor.close()
        connection.close()
        # print("Déconnexion")