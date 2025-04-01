import tkinter as tk
from tkinter import ttk, filedialog
from creation_module import PantallaPrincipal 
import sqlite3
from PIL import Image, ImageTk
from message_box import MessageBox  
import os  # Para manejar rutas de archivos
import json
import pandas as pd
from importation_module import DataImporter
from exportation_module import DataExporter
from edition_module import EdicionVentana
from deletion_module import delete_miniature


class PantallaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniBase v1.0.0")
        self.root.configure(bg="black")
        self.root.iconbitmap("MiniBase_Logo.ico")
        
        # Sobrescribir el evento de cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Maximizar la ventana al iniciar
        self.root.state('zoomed')
        
        # Crear el header con un borde blanco solo en la parte inferior
        self.header_frame = tk.Frame(self.root, bg="black")
        self.header_frame.pack(fill="x")

        # Línea divisoria en la parte inferior del header
        header_border = tk.Frame(self.header_frame, bg="white", height=2)  # Grosor de la línea
        header_border.pack(fill="x", side="bottom")

        # Botones en el header (cada botón se encierra en un frame con borde blanco)
        delete_button_frame = tk.Frame(self.header_frame, bg="white", padx=1, pady=1)
        delete_button_frame.pack(side="right", padx=10, pady=10)
        self.delete_button = tk.Button(
            delete_button_frame,
            text="Delete Mini",
            bg="black",
            fg="white",
            command=self.delete_selected_miniature
        )
        self.delete_button.pack()

        import_button_frame = tk.Frame(self.header_frame, bg="white", padx=1, pady=1)
        import_button_frame.pack(side="right", padx=10, pady=10)
        self.import_button = tk.Button(
            import_button_frame, 
            text="Import Data", 
            bg="black", 
            fg="white", 
            command=self.import_data
        )
        self.import_button.pack()

        export_button_frame = tk.Frame(self.header_frame, bg="white", padx=1, pady=1)
        export_button_frame.pack(side="right", padx=10, pady=10)
        self.export_button = tk.Button(
            export_button_frame, 
            text="Export Data", 
            bg="black", 
            fg="white", 
            command=self.export_data
        )
        self.export_button.pack()

        # Botón de Schema View en el header
        schema_button_frame = tk.Frame(self.header_frame, bg="white", padx=1, pady=1)
        schema_button_frame.pack(side="right", padx=10, pady=10)
        self.btn_schema = tk.Button(
            schema_button_frame,
            text="Schema View",
            bg="black",
            fg="white",
            command=self.open_schema_view
        )
        self.btn_schema.pack()

        refresh_button_frame = tk.Frame(self.header_frame, bg="white", padx=1, pady=1)
        refresh_button_frame.pack(side="right", padx=10, pady=10)
        self.refresh_button = tk.Button(
            refresh_button_frame, 
            text="Refresh DB", 
            bg="black", 
            fg="white", 
            command=self.refresh_screen
        )
        self.refresh_button.pack()
        
        new_button_frame = tk.Frame(self.header_frame, bg="white", padx=1, pady=1)
        new_button_frame.pack(side="right", padx=10, pady=10)
        self.new_button = tk.Button(
            new_button_frame, 
            text="Add New Mini", 
            bg="black", 
            fg="white", 
            command=self.open_pantalla_principal
        )
        self.new_button.pack()
        
        # Botón de edición en el header
        edit_button_frame = tk.Frame(self.header_frame, bg="white", padx=1, pady=1)
        edit_button_frame.pack(side="right", padx=10, pady=10)
        self.btn_editar = tk.Button(
            edit_button_frame,
            text="Edit Mini",
            bg="black",
            fg="white",
            command=self.abrir_edicion,
            state='disabled'
        )
        self.btn_editar.pack()
        
        # Cargar el logo
        self.logo_pil_image = Image.open("MiniBase_Logo.png").resize((100, 100), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(self.logo_pil_image)
        self.logo_label = tk.Label(self.header_frame, image=self.logo_image, bg="black", padx=10)
        self.logo_label.pack(side="left", padx=10, pady=10)
        
        # Título
        self.title_label = tk.Label(self.header_frame, bg="black", fg="white", text="MiniBase", font=("Helvetica", 22))
        self.title_label.pack(side="left", padx=10)
        
        # Crear el footer con un borde blanco solo en la parte superior
        self.footer_frame = tk.Frame(self.root, bg="black")
        self.footer_frame.pack(fill="x", side="bottom")
        footer_border = tk.Frame(self.footer_frame, bg="white", height=2)
        footer_border.pack(fill="x", side="top")
        self.title_label = tk.Label(self.footer_frame, bg="black", fg="white", text="Made with ♥ and Python", font=("Helvetica", 13))
        self.title_label.pack(side="top", padx=10)
        
        # Crear el content frame
        self.content_frame = tk.Frame(self.root, bg="black")
        self.content_frame.pack(fill="both", expand=True)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(2, weight=3)
        
        # Barra de búsqueda reestructurada
        self.search_frame = tk.Frame(self.content_frame, bg="black")
        self.search_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")
        # Configuramos tres columnas: izquierda (buscador), centro (contador) y derecha (vacío para balance)
        self.search_frame.grid_columnconfigure(0, weight=0)  # Fija para el buscador
        self.search_frame.grid_columnconfigure(1, weight=1)  # Se expande para centrar el contador
        self.search_frame.grid_columnconfigure(2, weight=0)  # Vacío

        # Frame izquierdo: buscador (Search: label y Entry)
        left_frame = tk.Frame(self.search_frame, bg="black")
        left_frame.grid(row=0, column=0, sticky="w")
        self.search_label = tk.Label(left_frame, text="Search:", bg="black", fg="white", font=("Helvetica", 13))
        self.search_label.pack(side="left", padx=5)
        self.search_entry = tk.Entry(left_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_miniatures)

        # Frame central: contador, centrado horizontalmente
        center_frame = tk.Frame(self.search_frame, bg="black")
        center_frame.grid(row=0, column=1, sticky="ew")
        center_frame.grid_columnconfigure(0, weight=1)
        self.count_label = tk.Label(center_frame, text="Miniatures in the database: 0", bg="black", fg="white", font=("Helvetica", 13))
        self.count_label.grid(row=0, column=0)

        # Frame derecho: se agrega el botón de información
        right_frame = tk.Frame(self.search_frame, bg="black")
        right_frame.grid(row=0, column=2, sticky="e")

        info_button = tk.Button(
            right_frame, 
            text="?", 
            bg="black", 
            fg="white", 
            font=("Helvetica", 13),
            command=self.open_info_window  # Función que abrirá la ventana de info
        )
        info_button.pack(padx=15)
        
        # Listbox de miniaturas
        self.listbox_frame = tk.Frame(self.content_frame, bg="black", bd=2, relief="sunken")
        self.listbox_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ns")
        self.listbox = tk.Listbox(self.listbox_frame, width=40, height=30)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.show_miniature_details)
        
        # Estilos personalizados para frames de labelframe
        style = ttk.Style()
        style.configure('Black.TLabelframe', background='black', foreground='white', font=('Helvetica', 13, 'bold'))
        style.configure('Black.TLabelframe.Label', background='black', foreground='white', font=('Helvetica', 16, 'bold'))

        # Frame de detalles de miniaturas
        self.details_frame = ttk.LabelFrame(self.content_frame, text="Details", style='Black.TLabelframe')
        self.details_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.details_label = tk.Label(self.details_frame, bg="black", fg="white", font=("Helvetica", 14, "bold"))
        self.details_label.pack(fill="x", pady=5)
        self.details_text = tk.Text(self.details_frame, bg="black", fg="white", font=("Helvetica", 13), wrap="word", state="disabled")
        self.details_text.pack(fill="both", expand=True)

        # Frame para fotografías
        self.photos_frame = ttk.LabelFrame(self.content_frame, text="Images", style='Black.TLabelframe')
        self.photos_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.canvas = tk.Canvas(self.photos_frame, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.prev_button = tk.Button(self.photos_frame, text="<<", command=self.prev_image, bg="black", fg="white")
        self.prev_button.pack(side="left", padx=5, pady=5)
        self.next_button = tk.Button(self.photos_frame, text=">>", command=self.next_image, bg="black", fg="white")
        self.next_button.pack(side="right", padx=5, pady=5)

        # Inicializar variables de imágenes
        self.images = []
        self.current_image_index = 0
        
        self.update_miniature_names()
        
    def update_miniature_names(self):
        """Actualizar la lista de nombres de miniaturas."""
        try:
            if not self.root.winfo_exists():
                return

            # Obtener los nombres actualizados desde la base de datos
            self.names = self.get_names()
            if self.listbox.winfo_exists():
                self.listbox.delete(0, tk.END)
                for id_name in self.names:
                    self.listbox.insert(tk.END, id_name[1])
                self.listbox.update_idletasks()
            
            # Actualizamos el contador de miniaturas
            self.count_label.config(text=f"Miniatures in the database: {len(self.names)}")
            
        except Exception as e:
            if self.root.winfo_exists():
                MessageBox.show_error(f"Error updating mini list: {e}")

    
    def refresh_screen(self):
        if not self.root.winfo_exists():
            return
        # Limpiar detalles e imágenes previas
        self.details_text.config(state="normal")
        self.details_text.delete("1.0", tk.END)
        self.details_text.config(state="disabled")
        self.canvas.delete("all")
        # Actualizar la lista de miniaturas
        self.update_miniature_names()

    def open_schema_view(self):
        from schemaview_module import SchemaView
        SchemaView(self.root)


    def open_info_window(self):
        # Abre la ventana de información usando el módulo info_window
        from info_window import InfoWindow  # Importación local para evitar dependencias circulares
        InfoWindow(self.root)
    
    def get_names(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = lambda cursor, row: (row[0], row[1])
            cursor = conn.cursor()
            # Nota: Nombre de la tabla en minúsculas
            cursor.execute('SELECT id, name FROM miniature')
            names = cursor.fetchall()
            conn.close()
            return names
        except Exception as e:
            MessageBox.show_error(f"Error fetching mini names: {e}")
            return []
    
    def filter_miniatures(self, event):
        search_text = self.search_entry.get().strip().lower()
        self.listbox.delete(0, tk.END)
        try:
            conn = sqlite3.connect("miniatures.db")
            # Configuramos el row_factory para obtener (id, name)
            conn.row_factory = lambda cursor, row: (row[0], row[1])
            cursor = conn.cursor()
            # Usar LIKE para filtrar (lower(name) para ignorar mayúsculas/minúsculas)
            cursor.execute("SELECT id, name FROM miniature WHERE lower(name) LIKE ?", ('%' + search_text + '%',))
            results = cursor.fetchall()
            conn.close()
            for id_name in results:
                # Insertar el nombre, limpiando espacios extras si fuera necesario
                self.listbox.insert(tk.END, id_name[1].strip())
        except Exception as e:
            MessageBox.show_error(f"Error filtering miniatures: {e}")

    
    def show_miniature_details(self, event):
        try:
            if not self.listbox.curselection():
                return

            selected_name = self.listbox.get(self.listbox.curselection())
            selected_id = None
            for id_name in self.names:
                if id_name[1] == selected_name:
                    selected_id = id_name[0]
                    break

            if selected_id:
                self.details_label.config(text=f"{selected_name}")
                self.update_miniature_details(selected_id)
                self.load_images(selected_id, selected_name)
                self.on_select_miniatura(selected_id)
        except Exception as e:
            MessageBox.show_error(f"Error displaying mini details: {e}")
    
    def update_miniature_details(self, miniature_id):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    m.name, l.designer, l.painted_by, l.label, l.lore_is_canon, 
                    l.character_origin, l.story, l.comment, l.year, l.code_or_reference, l.url,
                    v.weight, v.height, v.radius_of_base, v.material, v.main_color, 
                    v.secondary_color, v.shape, v.bioform
                FROM 
                    miniature m
                LEFT JOIN 
                    lore l ON m.id = l.miniature_id
                LEFT JOIN 
                    visual_metadata v ON m.id = v.miniature_id
                WHERE 
                    m.id = ?
            ''', (miniature_id,))
            result = cursor.fetchone()
            
            cursor.execute('''
                SELECT t.tag 
                FROM tags t
                JOIN miniature_tags mt ON t.id = mt.tag_id
                WHERE mt.miniature_id = ?
            ''', (miniature_id,))
            tags = cursor.fetchall()
            conn.close()
            
            if result:
                # Extraer campos de la fila (usando índices o nombres)
                name = result["name"]
                designer = result["designer"]
                painted_by = result["painted_by"]
                label = result["label"]
                lore_is_canon = result["lore_is_canon"]
                character_origin = result["character_origin"]
                story = result["story"]
                comment = result["comment"]
                year = result["year"]
                reference = result["code_or_reference"]
                url = result["url"]
                weight = result["weight"]
                height = result["height"]
                radius_of_base = result["radius_of_base"]
                material = result["material"]
                main_color = result["main_color"]
                secondary_color = result["secondary_color"]
                shape = result["shape"]
                bioform = result["bioform"]
                
                self.details_text.config(state="normal")
                self.details_text.delete("1.0", tk.END)
                
                # Crear el tag para negrita si no existe
                self.details_text.tag_configure("bold", font=("Helvetica", 13, "bold"))
                
                # Insertar texto con tags
                self.details_text.insert(tk.END, "Shape: ", "bold")
                self.details_text.insert(tk.END, f"{shape}\n")
                self.details_text.insert(tk.END, "Bioform: ", "bold")
                self.details_text.insert(tk.END, f"{bioform}\n")
                self.details_text.insert(tk.END, "Main Color: ", "bold")
                self.details_text.insert(tk.END, f"{main_color}\n")
                self.details_text.insert(tk.END, "Secondary Color: ", "bold")
                self.details_text.insert(tk.END, f"{secondary_color}\n")
                self.details_text.insert(tk.END, "Weight: ", "bold")
                self.details_text.insert(tk.END, f"{weight} g\n")
                self.details_text.insert(tk.END, "Height: ", "bold")
                self.details_text.insert(tk.END, f"{height} mm\n")
                self.details_text.insert(tk.END, "Radius of Base: ", "bold")
                self.details_text.insert(tk.END, f"{radius_of_base} mm\n")
                self.details_text.insert(tk.END, "Material: ", "bold")
                self.details_text.insert(tk.END, f"{material}\n")
                self.details_text.insert(tk.END, "Lore is Canon: ", "bold")
                self.details_text.insert(tk.END, f"{'Yes' if lore_is_canon else 'No'}\n")
                self.details_text.insert(tk.END, "Character Origin: ", "bold")
                self.details_text.insert(tk.END, f"{character_origin}\n")
                self.details_text.insert(tk.END, "Story: ", "bold")
                self.details_text.insert(tk.END, f"{story}\n")
                tags_text = ', '.join([tag["tag"] for tag in tags]) if tags else 'No tags'
                self.details_text.insert(tk.END, "Tags: ", "bold")
                self.details_text.insert(tk.END, f"{tags_text}\n")
                self.details_text.insert(tk.END, "Comment: ", "bold")
                self.details_text.insert(tk.END, f"{comment}\n")
                self.details_text.insert(tk.END, "Designer: ", "bold")
                self.details_text.insert(tk.END, f"{designer}\n")
                self.details_text.insert(tk.END, "Painted By: ", "bold")
                self.details_text.insert(tk.END, f"{painted_by}\n")
                self.details_text.insert(tk.END, "Label: ", "bold")
                self.details_text.insert(tk.END, f"{label}\n")
                self.details_text.insert(tk.END, "Year: ", "bold")
                self.details_text.insert(tk.END, f"{year}\n")
                self.details_text.insert(tk.END, "Reference: ", "bold")
                self.details_text.insert(tk.END, f"{reference}\n")
                self.details_text.insert(tk.END, "URL: ", "bold")
                self.details_text.insert(tk.END, f"{url}\n")
                
                self.details_text.config(state="disabled")
        except Exception as e:
            MessageBox.show_error(f"Error updating mini details: {e}")
    
    def load_images(self, selected_id, selected_name):
        try:
            self.images = []
            self.current_image_index = 0
            
            # Consulta las rutas de imagen guardadas en la base de datos para la miniatura seleccionada
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = lambda cursor, row: {cursor.description[idx][0]: row[idx] for idx in range(len(row))}
            cursor = conn.cursor()
            cursor.execute('''
                SELECT mv.url
                FROM miniature_views mv
                WHERE mv.miniature_id = ?
            ''', (selected_id,))
            rows = cursor.fetchall()
            conn.close()
            
            # Si no se encontraron registros, mostrar imagen por defecto
            if not rows:
                self._show_default_image()
                self.prev_button.config(state='disabled')
                self.next_button.config(state='disabled')
                return
            
            # Para cada ruta, se intenta cargar la imagen (solo si el archivo existe)
            for row in rows:
                image_path = row['url']
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image = image.resize((400, 400), Image.LANCZOS)
                    self.images.append(ImageTk.PhotoImage(image))
                else:
                    print(f"File not found: {image_path}")
            
            button_state = 'normal' if self.images else 'disabled'
            self.prev_button.config(state=button_state)
            self.next_button.config(state=button_state)
            
            if self.images:
                self.show_image(0)
            else:
                self._show_default_image()
        
        except Exception as e:
            MessageBox.show_error(f"Error loading mini images: {e}")
            self.canvas.delete("all")
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Error loading images",
                fill="red"
            )

    def _show_default_image(self):
        """Muestra una imagen por defecto si no hay imágenes válidas."""
        default_image_path = "images/no_image_available.png"
        if os.path.exists(default_image_path):
            default_image = Image.open(default_image_path)
            default_image = default_image.resize((200, 200), Image.LANCZOS)
            default_image_tk = ImageTk.PhotoImage(default_image)
            self.canvas.delete("all")
            self.canvas.create_image(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                anchor=tk.CENTER,
                image=default_image_tk
            )
            self.canvas.image = default_image_tk
        else:
            self.canvas.delete("all")
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="No images available",
                fill="white"
            )

    def show_image(self, index):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width = self.images[index].width()
        image_height = self.images[index].height()
        x = (canvas_width / 2) - (image_width / 2)
        y = (canvas_height / 2) - (image_height / 2)
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.images[index])
    
    def prev_image(self):
        if self.images and len(self.images) > 0:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.show_image(self.current_image_index)
    
    def next_image(self):
        if self.images and len(self.images) > 0:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.show_image(self.current_image_index)
    
    def open_pantalla_principal(self):
        root = tk.Toplevel(self.root)
        PantallaPrincipal(root)
    
    def import_data(self):
        DataImporter.import_data()

    def get_all_data(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    m.*, l.*, v.*
                FROM 
                    miniature m
                LEFT JOIN 
                    lore l ON m.id = l.miniature_id
                LEFT JOIN 
                    visual_metadata v ON m.id = v.miniature_id
            ''')
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            MessageBox.show_error(f"Error fetching data: {e}")
            return []
    def export_data(self):
        from tkinter import filedialog
        # Configura el diálogo para mostrar Excel, CSV y JSON
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json")
            ],
            title="Save File"
        )
        if file_path:
            from exportation_module import DataExporter
            exporter = DataExporter()
            if file_path.endswith(".xlsx"):
                exporter.export_to_excel_with_dialog(file_path)
            elif file_path.endswith(".csv"):
                exporter.export_to_csv_with_dialog(file_path)
            elif file_path.endswith(".json"):
                exporter.export_to_json_with_dialog(file_path)
            else:
                # En caso de que la extensión no sea ninguna de las anteriores
                MessageBox.show_warning("Unsupported format.")


    def delete_selected_miniature(self):
        try:
            if not self.listbox.curselection():
                MessageBox.show_warning("Please select a mini to delete")
                return

            selected_name = self.listbox.get(self.listbox.curselection())
            selected_id = next((id for id, name in self.names if name == selected_name), None)

            if selected_id and delete_miniature(selected_id, selected_name):
                self.canvas.delete("all")
                self.details_text.config(state="normal")
                self.details_text.delete("1.0", tk.END)
                self.details_text.config(state="disabled")
                self.update_miniature_names()
        except Exception as e:
            if self.root.winfo_exists():
                MessageBox.show_error(f"Error deleting mini: {e}")

    def abrir_edicion(self):
        if hasattr(self, 'miniatura_seleccionada'):
            EdicionVentana(self.root, self.miniatura_seleccionada)
            
    def on_select_miniatura(self, datos_miniatura):
        self.miniatura_seleccionada = datos_miniatura
        self.btn_editar.config(state='normal')

    def on_close(self):
        try:
            self.root.destroy()
        except Exception:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaInicio(root)
    root.mainloop()
