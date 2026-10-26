import tkinter as tk
from tkinter import messagebox


class RegisterView:

    def __init__(self, root):
        self.ventana = tk.Toplevel(root)

        # Configuración de la ventana con el mismo diseño que LoginView
        self.ventana.title("Registro de usuarios")
        self.ventana.geometry("530x530")
        self.ventana.configure(bg="#EDE7F6")
        self.ventana.resizable(False, False)

        # Mantener la ventana asociada a la principal
        self.ventana.transient(root)
        self.ventana.grab_set()

        # Título principal
        self.titulo = tk.Label(
            self.ventana,
            text="Crear Cuenta",
            font=("Times New Roman", 20, "bold"),
            bg="#EDE7F6",
            fg="#1D2786",
        )
        self.titulo.pack(pady=15)

        # Etiquetas y Campos de Entrada
        self.lbl_nombre = tk.Label(
            self.ventana,
            text="Nombre completo:",
            font=("Times New Roman", 11),
            bg="#EDE7F6",
        )
        self.lbl_nombre.pack()

        self.entry_nombre = tk.Entry(
            self.ventana, width=35, font=("Arial", 11)
        )
        self.entry_nombre.pack(pady=3)

        self.lbl_email = tk.Label(
            self.ventana,
            text="Correo electrónico:",
            font=("Times New Roman", 11),
            bg="#EDE7F6",
        )
        self.lbl_email.pack()

        self.entry_email = tk.Entry(
            self.ventana, width=35, font=("Arial", 11)
        )
        self.entry_email.pack(pady=3)

        self.lbl_password = tk.Label(
            self.ventana,
            text="Contraseña:",
            font=("Times New Roman", 11),
            bg="#EDE7F6",
        )
        self.lbl_password.pack()

        self.entry_password = tk.Entry(
            self.ventana, width=35, font=("Arial", 11), show="*"
        )
        self.entry_password.pack(pady=3)

        self.lbl_confirmar = tk.Label(
            self.ventana,
            text="Confirmar contraseña:",
            font=("Times New Roman", 11),
            bg="#EDE7F6",
        )
        self.lbl_confirmar.pack()

        self.entry_confirmar = tk.Entry(
            self.ventana, width=35, font=("Arial", 11), show="*"
        )
        self.entry_confirmar.pack(pady=3)

        # Botón Principal (Registrar usuario)
        self.btn_guardar = tk.Button(
            self.ventana,
            text="Registrar usuario",
            width=25,
            bg="#40128B",
            fg="white",
            font=("Times New Roman", 11, "bold"),
            cursor="hand2",
            command=self.guardar_usuario,
        )
        self.btn_guardar.pack(pady=15)

        # Botón Secundario (Cancelar)
        self.btn_cancelar = tk.Button(
            self.ventana,
            text="Cancelar",
            width=20,
            bg="#B2A4FF",
            fg="white",
            font=("Times New Roman", 10),
            cursor="hand2",
            command=self.cerrar,
        )
        self.btn_cancelar.pack()

        self.entry_nombre.focus_set()

    def obtener_datos(self):
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        confirmar = self.entry_confirmar.get()

        return nombre, email, password, confirmar

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(titulo, mensaje, parent=self.ventana)
        else:
            messagebox.showinfo(titulo, mensaje, parent=self.ventana)

    def guardar_usuario(self):
        nombre, email, password, confirmar = self.obtener_datos()

        if not nombre or not email or not password or not confirmar:
            self.mostrar_mensaje(
                "Atención", "Todos los campos son obligatorios", "error"
            )
            return

        if password != confirmar:
            self.mostrar_mensaje(
                "Error", "Las contraseñas no coinciden", "error"
            )
            return

        try:
            from models.user_model import UserModel

            model = UserModel()
            resultado = model.registrar_usuario(nombre, email, password)

            if resultado == "ok":
                self.mostrar_mensaje(
                    "Éxito", "Usuario registrado correctamente"
                )
                self.cerrar()
            elif resultado == "duplicado":
                self.mostrar_mensaje(
                    "Error",
                    "El correo electrónico ya está registrado",
                    "error",
                )
            else:
                self.mostrar_mensaje(
                    "Error", "No se pudo registrar el usuario", "error"
                )

        except Exception as e:
            self.mostrar_mensaje("Error", f"Error de conexión: {e}", "error")

    def cerrar(self):
        self.ventana.destroy()