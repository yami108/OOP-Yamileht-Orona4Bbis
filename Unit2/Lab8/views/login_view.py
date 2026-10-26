import os
import tkinter as tk  
from tkinter import messagebox
from PIL import Image, ImageTk


class LoginView:

    def __init__(self, root):
        self.root = root

        # PERSONALIZAR 1:
        # Cambia el título de la ventana.
        self.root.title("Iniciar sesion")

        # PERSONALIZAR 2:
        # Modifica el ancho y alto de la ventana.
        self.root.geometry("530x530")

        # PERSONALIZAR 3:
        # Cambia el color de fondo.
        self.root.configure(bg="#EDE7F6")

        self.root.resizable(False, False)

        # PERSONALIZAR 4:
        # Cambia el texto, la fuente y los colores del título.
        self.titulo = tk.Label(
            root,
            text="Iniciar Sesion",
            font=("Times New Roman", 20, "bold"),
            bg="#EDE7F6",
            fg="#1D2786",
        )
        self.titulo.pack(pady=20)

        # PERSONALIZAR 5:
        # Modifica el texto y la apariencia de las etiquetas.
        self.lbl_email = tk.Label(
            root,
            text="Email:",
            font=("Times New Roman", 11),
            bg="#EDE7F6",
        )
        self.lbl_email.pack()

        # PERSONALIZAR 6:
        # Cambia el ancho, la fuente y otros atributos del campo.
        self.entry_email = tk.Entry(
            root, width=30, font=("Arial", 11)
        )
        self.entry_email.pack(pady=5)

        self.lbl_password = tk.Label(
            root,
            text="Contraseña:",
            font=("Times New Roman", 11),
            bg="#EDE7F6",
        )
        self.lbl_password.pack()

        # El atributo show oculta los caracteres al escribir.
        self.entry_password = tk.Entry(
            root, width=35, font=("Arial", 11), show="*"
        )
        self.entry_password.pack(pady=5)

        # PERSONALIZAR 7:
        # Cambia el texto, color, tamaño y fuente del botón.
        self.btn_login = tk.Button(
            root,
            text="Ingresar",
            width=25,
            bg="#40128B",
            fg="white",
            font=("Times New Roman", 11, "bold"),
            cursor="hand2",
            command=self.login_action,  # <-- Se asignó la acción del botón
        )
        self.btn_login.pack(pady=15)

        # PERSONALIZAR 8:
        # Cambia el diseño del botón para abrir el registro.
        self.btn_register = tk.Button(
            root,
            text="Crear cuenta",
            width=20,
            bg="#B2A4FF",
            fg="white",
            font=("Times New Roman", 10),
            cursor="hand2",
            command=self.abrir_registro,  # <-- Se asignó la acción del botón
        )
        self.btn_register.pack()

    def obtener_datos(self):
        email = self.entry_email.get().strip()
        password = self.entry_password.get()

        return email, password

    def limpiar_campos(self):
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "error":
            messagebox.showerror(titulo, mensaje, parent=self.root)
        else:
            messagebox.showinfo(titulo, mensaje, parent=self.root)

    # --- NUEVAS FUNCIONES DE MANEJO DE EVENTOS ---

    def login_action(self):
        """Maneja el clic en el botón Ingresar"""
        email, password = self.obtener_datos()

        if not email or not password:
            self.mostrar_mensaje(
                "Atención",
                "Por favor completa todos los campos.",
                tipo="error",
            )
            return

        # Aquí conectas con la lógica de validación o controlador
        self.mostrar_mensaje(
            "Éxito", f"Iniciando sesión con el correo: {email}"
        )

    def abrir_registro(self):
        """Maneja el clic en el botón Crear cuenta"""
        try:
            from views.registres_view import RegisterView

            RegisterView(self.root)
        except ModuleNotFoundError:
            # En caso de que la ruta varíe según la estructura del proyecto
            from registres_view import RegisterView

            RegisterView(self.root)