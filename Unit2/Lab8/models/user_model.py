import psycopg2
from controllers.connection_controler import Conexion


class UserModel:

    def __init__(self):
        self.conexion_db = Conexion()

    def registrar_usuario(self, nombre, email, password):
        conexion = self.conexion_db.conectar()

        if conexion is None:
            return "error"

        cursor = None

        try:
            cursor = conexion.cursor()

            # Nombres de columnas corregidos según tu DB:
            # nombre, username, passw
            consulta = """
                INSERT INTO users (nombre, username, passw)
                VALUES (%s, %s, %s)
            """

            cursor.execute(consulta, (nombre, email, password))
            conexion.commit()

            return "ok"

        except psycopg2.IntegrityError as error:
            print("Error de Integridad (usuario/email duplicado):", error)
            return "duplicado"

        except Exception as error:
            print("Error exacto en la base de datos:", error)
            return "error"

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

    def validar_usuario(self, email, password):
        conexion = self.conexion_db.conectar()

        if conexion is None:
            return None

        cursor = None

        try:
            cursor = conexion.cursor()

            # Nombres de columnas corregidos: id_user, nombre, username, passw
            consulta = """
                SELECT id_user, nombre
                FROM users
                WHERE username = %s AND passw = %s
            """

            cursor.execute(consulta, (email, password))
            usuario = cursor.fetchone()

            return usuario

        except Exception as error:
            print("Error al validar usuario:", error)
            return None

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None:
                conexion.close()

    def cerrar(self):
        # Cada operación cierra su propia conexión.
        # Se conserva este método para mantener la interfaz del controlador sencilla.
        pass