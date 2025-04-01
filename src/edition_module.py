import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from message_box import MessageBox
from photo_uploader import upload_photos

class VentanaFotos(tk.Toplevel):
    def __init__(self, parent, miniature_id):
        super().__init__(parent)
        self.title("Edit images")
        self.miniature_id = miniature_id
        self.configure(bg="black")  # Fondo negro para la ventana
        
        # Configurar estilo para los frames y labels
        style = ttk.Style()
        style.configure('Black.TFrame', background='black')
        style.configure('Black.TLabelframe', background='black', foreground='white', font=('Helvetica', 14, 'bold'))
        style.configure('Black.TLabelframe.Label', background='black', foreground='white', font=('Helvetica', 16, 'bold'))
        
        # Frame principal
        self.frame_principal = ttk.Frame(self, padding="20", style='Black.TFrame')
        self.frame_principal.pack(expand=True, fill='both')
        
        # Cargar fotos existentes
        self.cargar_fotos_existentes()
        # Crear la sección de fotos
        self.crear_seccion_fotos()

    def cargar_fotos_existentes(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = lambda cursor, row: {cursor.description[idx][0]: row[idx] for idx in range(len(row))}
            cursor = conn.cursor()
            
            # Obtener las fotos existentes y sus tipos
            cursor.execute('''
                SELECT vt.view_type, mv.url
                FROM miniature_views mv
                JOIN view_types vt ON mv.view_type_id = vt.id
                WHERE mv.miniature_id = ?
            ''', (self.miniature_id,))
            
            self.fotos_existentes = {row['view_type']: row['url'] for row in cursor.fetchall()}
            conn.close()
            
        except Exception as e:
            MessageBox.show_error(message=f"Error uploading existing images: {str(e)}")
            self.fotos_existentes = {}

    def crear_seccion_fotos(self):
        photos_section = ttk.LabelFrame(
            self.frame_principal, 
            text="Edit Images",
            padding=10,
            style='Black.TLabelframe'
        )
        photos_section.pack(fill="x", padx=10, pady=5)
        
        self.url_entries = {}
        
        self.entry_image_info = [
            "Frontal", "Black Background", "White Background", "Lateral View 1", 
            "Lateral View 2", "Back View", "Top View", "Bottom View", 
            "Close-up View", "Isometric View", "3D Model View", "Video or GIF", 
            "Other View"
        ]

        
        for view_type in self.entry_image_info:
            row_frame = ttk.Frame(photos_section, style='Black.TFrame')
            row_frame.pack(fill="x", pady=2)
            
            tk.Label(
                row_frame,
                text=view_type,
                bg="black",
                fg="white"
            ).pack(side="left", padx=5)
            
            entry = ttk.Entry(row_frame, width=50)
            if view_type in self.fotos_existentes:
                entry.insert(0, self.fotos_existentes[view_type])
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.url_entries[view_type] = entry
            
            tk.Button(
                row_frame, 
                text="Browse", 
                bg="black",
                fg="white",
                command=lambda e=entry: self.browse_file(e)
            ).pack(side="left", padx=5)

            
            if view_type in self.fotos_existentes:
                tk.Label(
                    row_frame,
                    text="✓",
                    bg="black",
                    fg="green"
                ).pack(side="left", padx=5)
        
        upload_button_frame = tk.Frame(photos_section, bg="black", padx=1, pady=1)
        upload_button_frame.pack(pady=10)
        
        tk.Button(
            upload_button_frame,
            text="Upload Images",
            bg="black",
            fg="white",
            command=self.guardar_fotos
        ).pack()

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)

    def guardar_fotos(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            cursor = conn.cursor()
            
            # Obtener el nombre de la miniatura
            cursor.execute('SELECT name FROM miniature WHERE id = ?', (self.miniature_id,))
            result = cursor.fetchone()
            if result:
                miniature_name = result[0] if isinstance(result, tuple) else result["name"]
            else:
                MessageBox.show_error(message="Miniature not found")
                conn.close()
                return
            
            # Construir un diccionario final con las rutas a guardar.
            # Si la ruta ingresada es la misma que la ya guardada, se reutiliza.
            # Si es distinta (o nueva), se sube la foto nuevamente.
            final_image_paths = {}
            for view_type in self.entry_image_info:
                entry = self.url_entries[view_type]
                current_path = entry.get().strip()
                if current_path:
                    if view_type in self.fotos_existentes and current_path == self.fotos_existentes[view_type]:
                        # La foto no ha sido modificada, se conserva la ruta existente.
                        final_image_paths[view_type] = current_path
                    else:
                        # La foto fue modificada o es nueva; se sube la foto.
                        # Se envía un diccionario con solo esta vista para obtener la ruta procesada.
                        new_uploaded = upload_photos(self.miniature_id, miniature_name, **{view_type: current_path})
                        if new_uploaded.get(view_type):
                            final_image_paths[view_type] = new_uploaded[view_type]
            
            if not final_image_paths:
                MessageBox.show_info(message="There are no changes to the images to save.")
                conn.close()
                return
            
            # Actualizar la base de datos:
            # Por cada vista en final_image_paths se elimina la fila existente y se inserta la nueva.
            for view_type, image_filename in final_image_paths.items():
                cursor.execute('SELECT id FROM view_types WHERE view_type = ?', (view_type,))
                res = cursor.fetchone()
                if res:
                    view_type_id = res[0] if isinstance(res, tuple) else res["id"]
                    # Borrar la fila anterior (si existe)
                    cursor.execute('DELETE FROM miniature_views WHERE miniature_id = ? AND view_type_id = ?', (self.miniature_id, view_type_id))
                    # Insertar la nueva ruta
                    cursor.execute('INSERT INTO miniature_views (miniature_id, view_type_id, url) VALUES (?, ?, ?)',
                                (self.miniature_id, view_type_id, image_filename))
                else:
                    print(f"Warning: View type '{view_type}' no encontrado en la base de datos")
            
            conn.commit()
            conn.close()
            MessageBox.show_info(message="Images updated successfully")
            # Actualizar la información de fotos y checkmarks
            self.cargar_fotos_existentes()
            self.actualizar_checkmarks()
        
        except Exception as e:
            MessageBox.show_error(message=f"Error saving images: {e}")
            
    def limpiar_entries(self):
        for entry in self.url_entries.values():
            entry.delete(0, tk.END)

    def actualizar_checkmarks(self):
        for view_type, entry in self.url_entries.items():
            if view_type in self.fotos_existentes:
                parent = entry.master
                for widget in parent.winfo_children():
                    if isinstance(widget, tk.Label) and widget["text"] == "✓":
                        widget.destroy()
                tk.Label(
                    parent,
                    text="✓",
                    bg="black",
                    fg="green"
                ).pack(side="left", padx=5)


class EdicionVentana(tk.Toplevel):
    def __init__(self, parent, miniature_id):
        super().__init__(parent)
        self.title("Edit all details")
        self.state('zoomed')
        self.configure(bg="black")
        self.miniature_id = miniature_id
        
        style = ttk.Style()
        style.configure('Black.TFrame', background='black')
        style.configure('Black.TLabelframe', background='black', foreground='white', font=('Helvetica', 14, 'bold'))
        style.configure('Black.TLabelframe.Label', background='black', foreground='white', font=('Helvetica', 16, 'bold'))
        style.configure('TCheckbutton', background='black', foreground='white')
        
        self.frame_principal = ttk.Frame(self, padding="20", style='Black.TFrame')
        self.frame_principal.grid(row=0, column=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.get_tags()
        self.get_miniature_tags()
        
        self.campos = {}
        self.cargar_datos()
        self.crear_campos()
        
        self.frame_botones = ttk.Frame(self.frame_principal, style='Black.TFrame')
        self.frame_botones.grid(row=1, column=0, columnspan=2, pady=20)


    def abrir_editor_fotos(self):
        VentanaFotos(self, self.miniature_id)

    def get_tags(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = lambda cursor, row: row  # Tuplas
            cursor = conn.cursor()
            cursor.execute('SELECT id, tag FROM tags')
            self.tags_data = cursor.fetchall()
            self.tags = [tag[1] for tag in self.tags_data]
            conn.close()
        except Exception as e:
            MessageBox.show_error(message=f"Error getting tags: {str(e)}")
            self.tags = []
            self.tags_data = []

    def get_miniature_tags(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = lambda cursor, row: row  # Tuplas
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, t.tag 
                FROM tags t
                JOIN miniature_tags mt ON t.id = mt.tag_id
                WHERE mt.miniature_id = ?
            ''', (self.miniature_id,))
            self.current_tags = cursor.fetchall()
            conn.close()
        except Exception as e:
            MessageBox.show_error(message=f"Error getting current tags: {str(e)}")
            self.current_tags = []

    def cargar_datos(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = lambda cursor, row: {cursor.description[idx][0]: row[idx] for idx in range(len(row))}
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    m.name,
                    v.weight, v.height, v.radius_of_base, v.material, 
                    v.main_color, v.secondary_color, v.shape, v.bioform,
                    l.designer, l.painted_by, l.label, l.lore_is_canon, 
                    l.character_origin, l.story, l.comment, l.year, 
                    l.code_or_reference, l.url
                FROM miniature m
                LEFT JOIN visual_metadata v ON m.id = v.miniature_id
                LEFT JOIN lore l ON m.id = l.miniature_id
                WHERE m.id = ?
            ''', (self.miniature_id,))
            
            self.datos = cursor.fetchone()
            conn.close()
            
        except Exception as e:
            MessageBox.show_error(message=f"Error loading data: {str(e)}")

    def crear_campos(self):
        sections = {
            "left_column": {
                "Name & Tags": ["name", "tag"],
                "Visual Data": ["weight", "height", "radius_of_base", "material", "main_color", 
                                "secondary_color", "shape", "bioform"]
            },
            "right_column": {
                "Some Lore About Your Piece": ["designer", "painted_by", "label", "lore_is_canon", 
                                        "character_origin", "story", "comment", "year", 
                                        "code_or_reference", "url"]
            }
        }
        
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=1, pad=20)
        
        left_column = ttk.Frame(self.frame_principal, style='Black.TFrame')
        left_column.grid(row=0, column=0, sticky='nsew', padx=5)
        
        right_column = ttk.Frame(self.frame_principal, style='Black.TFrame')
        right_column.grid(row=0, column=1, sticky='nsew', padx=5)
        
        for section_name, fields in sections["left_column"].items():
            section_frame = ttk.LabelFrame(
                left_column,
                text=section_name,
                padding=10,
                style='Black.TLabelframe'
            )
            section_frame.pack(fill="x", pady=5)
            self._crear_campos_seccion(section_frame, fields)
        
        for section_name, fields in sections["right_column"].items():
            section_frame = ttk.LabelFrame(
                right_column,
                text=section_name,
                padding=10,
                style='Black.TLabelframe'
            )
            section_frame.pack(fill="both", expand=True, pady=5)
            self._crear_campos_seccion(section_frame, fields)
            
            if section_name == "Some Lore About Your Piece":
                edit_photos_frame = tk.Frame(section_frame, bg="white", padx=1, pady=1)
                edit_photos_frame.pack(pady=10)
                
                tk.Button(
                    edit_photos_frame,
                    text="Verify, replace or upload images",
                    bg="black",
                    fg="white",
                    command=self.abrir_editor_fotos
                ).pack()
        
        buttons_frame = ttk.Frame(right_column, style='Black.TFrame')
        buttons_frame.pack(fill='x', pady=20)
        center_container = ttk.Frame(buttons_frame, style='Black.TFrame')
        center_container.pack(expand=True, anchor='center')
        
        save_frame = tk.Frame(center_container, bg="white", padx=1, pady=1)
        save_frame.pack(side='left', padx=10)
        tk.Button(
            save_frame,
            text="Save & Close",
            bg="black",
            fg="white",
            command=self.guardar_cambios
        ).pack()
        
        cancel_frame = tk.Frame(center_container, bg="white", padx=1, pady=1)
        cancel_frame.pack(side='left')
        tk.Button(
            cancel_frame,
            text="Cancel",
            bg="black",
            fg="white",
            command=self.destroy
        ).pack()

    def _crear_campos_seccion(self, section_frame, fields):
        for field in fields:
            frame = ttk.Frame(section_frame, style='Black.TFrame')
            frame.pack(fill="x", pady=2)
            
            tk.Label(
                frame,
                text=field.replace('_', ' ').title(),
                bg="black",
                fg="white"
            ).pack(side='left', padx=5)
            
            if field == 'lore_is_canon':
                var = tk.BooleanVar(value=self.datos.get(field, False))
                radio_frame = ttk.Frame(frame, style='Black.TFrame')
                radio_frame.pack(side='left', fill='x', expand=True, padx=5)
                
                ttk.Radiobutton(
                    radio_frame,
                    text="Yes",
                    variable=var,
                    value=True,
                    style='TCheckbutton'
                ).pack(side='left', padx=10)
                
                ttk.Radiobutton(
                    radio_frame,
                    text="No",
                    variable=var,
                    value=False,
                    style='TCheckbutton'
                ).pack(side='left', padx=10)
                
                self.campos[field] = var
            elif field == 'tag':
                tags_container = ttk.Frame(frame, style='Black.TFrame')
                tags_container.pack(side='left', fill='both', expand=True, padx=5)
                self.tag_vars = {}
                row = 0
                col = 0
                max_cols = 3
                for tag_id, tag_name in self.tags_data:
                    var = tk.BooleanVar()
                    self.tag_vars[tag_id] = var
                    for current_tag in self.current_tags:
                        if tag_id == current_tag[0]:
                            var.set(True)
                            break
                    cb = ttk.Checkbutton(
                        tags_container,
                        text=tag_name,
                        variable=var,
                        style='TCheckbutton'
                    )
                    cb.grid(row=row, column=col, sticky='w', padx=5, pady=2)
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                self.campos['tag'] = self.tag_vars
            else:
                entrada = ttk.Entry(frame, width=50)
                entrada.insert(0, str(self.datos.get(field, '')))
                self.campos[field] = entrada
                entrada.pack(side='left', fill='x', expand=True, padx=5)

    def guardar_cambios(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            cursor = conn.cursor()
            
            tag_ids = [tag_id for tag_id, var in self.tag_vars.items() if var.get()]
            if not tag_ids:
                MessageBox.show_error(message="Please select at least one tag")
                return

            cursor.execute('''
                UPDATE miniature 
                SET name = ?
                WHERE id = ?
            ''', (
                self.campos['name'].get(),
                self.miniature_id
            ))
            
            cursor.execute('DELETE FROM miniature_tags WHERE miniature_id = ?', (self.miniature_id,))
            for tag_id in tag_ids:
                cursor.execute('''
                    INSERT INTO miniature_tags (miniature_id, tag_id) 
                    VALUES (?, ?)
                ''', (self.miniature_id, tag_id))
            
            cursor.execute('''
                UPDATE visual_metadata 
                SET weight = ?, height = ?, radius_of_base = ?, 
                    material = ?, main_color = ?, secondary_color = ?, 
                    shape = ?, bioform = ?
                WHERE miniature_id = ?
            ''', (
                self.campos['weight'].get(),
                self.campos['height'].get(),
                self.campos['radius_of_base'].get(),
                self.campos['material'].get(),
                self.campos['main_color'].get(),
                self.campos['secondary_color'].get(),
                self.campos['shape'].get(),
                self.campos['bioform'].get(),
                self.miniature_id
            ))
            
            cursor.execute('''
                UPDATE lore 
                SET designer = ?, painted_by = ?, label = ?, 
                    lore_is_canon = ?, character_origin = ?, story = ?,
                    comment = ?, year = ?, code_or_reference = ?, url = ?
                WHERE miniature_id = ?
            ''', (
                self.campos['designer'].get(),
                self.campos['painted_by'].get(),
                self.campos['label'].get(),
                self.campos['lore_is_canon'].get(),
                self.campos['character_origin'].get(),
                self.campos['story'].get(),
                self.campos['comment'].get(),
                self.campos['year'].get(),
                self.campos['code_or_reference'].get(),
                self.campos['url'].get(),
                self.miniature_id
            ))
            
            conn.commit()
            conn.close()
            
            MessageBox.show_info(message="Miniature updated successfully")
            self.destroy()
            
        except Exception as e:
            MessageBox.show_error(message=f"Error updating: {str(e)}")
