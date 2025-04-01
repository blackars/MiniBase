import tkinter as tk

class MessageBox:
    def __init__(self, title, message, type_="info"):
        self.root = tk.Toplevel()
        self.root.title(title)
        self.root.configure(bg="black")
        self.root.iconbitmap("MiniBase_Logo.ico")

        
        # Hacer que la ventana sea modal y asegurar que se cierre correctamente
        self.root.transient()
        self.root.grab_set()
        self.root.focus_force()

        # Calculamos el ancho basado en la longitud del mensaje
        message_width = min(max(len(message) * 10, 200), 600)  # Mínimo 200px, máximo 600px
        
        self.label = tk.Label(self.root, text=message, fg="white", bg="black", 
                            font=("Arial", 12), wraplength=message_width)
        self.label.pack(padx=20, pady=20)

        if type_ == "error":
            self.button = tk.Button(self.root, text="OK", command=self.root.destroy, fg="white", bg="red")
        elif type_ == "warning":
            self.button = tk.Button(self.root, text="OK", command=self.root.destroy, fg="white", bg="orange")
        elif type_ == "confirmation":
            self.button_yes = tk.Button(self.root, text="Sí", command=lambda: self.return_value(True), fg="white", bg="green")
            self.button_no = tk.Button(self.root, text="No", command=lambda: self.return_value(False), fg="white", bg="red")
            self.button_yes.pack(side=tk.LEFT, padx=10, pady=10)
            self.button_no.pack(side=tk.RIGHT, padx=10, pady=10)
        else:
            self.button = tk.Button(self.root, text="OK", command=self.root.destroy, fg="white", bg="blue")

        if type_ != "confirmation":
            self.button.pack(pady=10)

        # Ajustar el tamaño de la ventana al contenido
        self.root.update()
        window_width = max(self.label.winfo_reqwidth() + 40, 200)  # Añadir padding
        window_height = self.label.winfo_reqheight() + 80  # Espacio para botones y padding
        
        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Evitar mainloop y usar wait_window en su lugar
        self.root.wait_window()

    def return_value(self, value):
        self.result = value
        self.root.destroy()

    @staticmethod
    def show_error(message):
        if tk._default_root and tk._default_root.winfo_exists():
            MessageBox("Error", message, "error")

    @staticmethod
    def show_info(message):
        if tk._default_root and tk._default_root.winfo_exists():
            MessageBox("Information", message, "info")

    @staticmethod
    def show_warning(message):
        MessageBox("Warning", message, "warning")

    @staticmethod
    def ask_confirmation(message):
        box = MessageBox("Confirmation", message, "confirmation")
        return box.result  # Devuelve True o False según la elección del usuario

# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    MessageBox.show_info("This is an information message.")
    MessageBox.show_error("An error has occurred.")
    MessageBox.show_warning("Be careful with this action.")
    respuesta = MessageBox.ask_confirmation("Are you sure you want to continue?")
    print("Answer:", respuesta)
