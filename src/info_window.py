import tkinter as tk
from tkinter import ttk, scrolledtext
import os

class InfoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Information - README.md")
        self.configure(bg="black")
        self.geometry("600x400")
        
        # Configurar estilos
        style = ttk.Style(self)
        style.configure("Black.TFrame", background="black")
        style.configure("Black.TLabel", background="black", foreground="white", font=("Helvetica", 12))
        style.configure("Black.TButton", background="black", foreground="white", font=("Helvetica", 12))
        
        # Frame contenedor
        container = ttk.Frame(self, style="Black.TFrame")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área de texto con scroll para mostrar el README.md
        self.text_area = scrolledtext.ScrolledText(
            container, wrap=tk.WORD, 
            bg="black", fg="white", 
            font=("Helvetica", 10)
        )
        self.text_area.pack(fill="both", expand=True)
        self.text_area.config(state="disabled")
        
        # Cargar el contenido del README.md
        self.load_readme()
    
    def load_readme(self):
        readme_path = "TECHNOLOGY.md"
        if os.path.exists(readme_path):
            try:
                with open(readme_path, "r", encoding="utf-8") as file:
                    content = file.read()
            except Exception as e:
                content = f"Error reading README.md: {e}"
        else:
            content = "README.md not found."
        
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, content)
        self.text_area.config(state="disabled")
