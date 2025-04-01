import tkinter as tk
from home_screen import PantallaInicio
from tkinter import *
import os   
from tkinter import messagebox

def load_images(self, selected_id, selected_name):
    try:
        # Construir la ruta de la carpeta de imágenes
        folder_path = os.path.join("images", f"{selected_id}_{selected_name}")
        
        # Verificar si la carpeta existe
        if not os.path.exists(folder_path):
            messagebox.showwarning("Warning", f"The image folder was not found for: {selected_name}")
            return  # Salir del método si la carpeta no existe
        
        # Cargar imágenes desde la carpeta
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                # Aquí puedes cargar la imagen con Pillow o cualquier otra lógica
                print(f"Loading image: {file_path}")
        
    except Exception as e:
        messagebox.showerror("Unexpected error", f"Error loading images: {e}")

# Crear una instancia de la clase Tk
root = tk.Tk()
root.geometry("900x600")    
root['background']='black'

# Crear el header con un borde blanco solo en la parte inferior
header_frame = tk.Frame(root, bg="black")   
header_frame.pack(fill="x")

# Línea divisoria en la parte inferior del header
header_border = tk.Frame(header_frame, bg="white", height=2)  # Grosor de la línea
header_border.pack(fill="x", side="bottom")

# Crear el footer con un borde blanco solo en la parte superior
footer_frame = tk.Frame(root, bg="black")
footer_frame.pack(fill="x", side="bottom")

# Línea divisoria en la parte superior del footer
footer_border = tk.Frame(footer_frame, bg="white", height=2)  # Grosor de la línea
footer_border.pack(fill="x", side="top")

# Crear una instancia de la clase PantallaInicio
pantalla_inicio = PantallaInicio(root)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
