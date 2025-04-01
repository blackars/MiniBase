import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import shutil

# Importar PhotoUploader y MessageBox (asegúrate de que los archivos existan en tu proyecto)
from photo_uploader import upload_photos
from message_box import MessageBox

# -------------------- Creation Module 1 --------------------
class PantallaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Add New Miniature")
        self.root.configure(bg="black")
        self.root.state('zoomed')
        
        self.outer_frame = tk.Frame(root, bg="black")
        self.outer_frame.pack(expand=True, fill='both')
        self.center_frame = tk.Frame(self.outer_frame, bg="black")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.frame = tk.Frame(self.center_frame, bg="black")
        self.frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.subtitle_label = tk.Label(self.frame, text="Please fill in the details below to add a new miniature.", 
                                    font=("Helvetica", 13), fg="white", bg="black", wraplength=600)
        self.subtitle_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        style = ttk.Style()
        style.configure('Black.TLabelframe', background='black', foreground='white', font=('Helvetica', 14, 'bold'))
        style.configure('Black.TLabelframe.Label', background='black', foreground='white', font=('Helvetica', 14, 'bold'))
        
        self.form_frame = ttk.LabelFrame(self.frame, text="Add New Miniature Details", padding=10, style='Black.TLabelframe')
        self.form_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="nsew")
        
        self.create_label_and_entry(self.form_frame, "Name:", 0)
        self.create_label_and_entry(self.form_frame, "Bioform:", 1)
        self.create_label_and_entry(self.form_frame, "Shape:", 2)
        self.create_label_and_entry(self.form_frame, "Height in mm:", 3)
        self.create_label_and_entry(self.form_frame, "Weight in g:", 4)
        self.create_label_and_entry(self.form_frame, "Radius of base in mm:", 5)
        self.create_label_and_entry(self.form_frame, "Material:", 6)
        self.create_label_and_entry(self.form_frame, "Main Color:", 7)
        self.create_label_and_entry(self.form_frame, "Secondary Color:", 8)
        self.create_label_and_combobox(self.form_frame, "Tags:", 9)
        
        self.button = tk.Button(self.form_frame, text="Next", bg="black", fg="white", command=self.abrir_segunda_pantalla)
        self.button.grid(row=10, column=0, columnspan=2, pady=20)
        self.form_frame.columnconfigure(1, weight=1)
    
    def create_label_and_entry(self, parent, text, row):
        label = tk.Label(parent, text=text, bg="black", fg="white", width=20, anchor="w")
        label.grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(parent, width=30)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        field_mapping = {
            "Height in mm:": "height",
            "Weight in g:": "weight",
            "Radius of base in mm:": "radius_of_base",
            "Main Color:": "main_color",
            "Secondary Color:": "secondary_color",
            "Name:": "name",
            "Bioform:": "bioform",
            "Shape:": "shape",
            "Material:": "material"
        }
        attr_name = field_mapping.get(text, text.lower().replace(':', '').replace(' ', '_'))
        setattr(self, f"{attr_name}_entry", entry)
    
    def create_label_and_combobox(self, parent, text, row):
        label = tk.Label(parent, text=text, bg="black", fg="white", width=20, anchor="w")
        label.grid(row=row, column=0, padx=5, pady=5, sticky="e")
        list_frame = tk.Frame(parent, bg="black")
        list_frame.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Listbox(list_frame, selectmode="multiple", height=4, width=27, yscrollcommand=scrollbar.set)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)
        for tag in self.get_tags():
            listbox.insert(tk.END, tag)
        attr_name = text.lower().replace(':', '').replace(' ', '_')
        setattr(self, f"{attr_name}_listbox", listbox)
    
    def get_tags(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            cursor = conn.cursor()
            cursor.execute('SELECT id, tag FROM tags')
            tags = cursor.fetchall()
            conn.close()
            return [tag[1] for tag in tags]
        except Exception as e:
            MessageBox.show_error(f"Error getting tags: {e}")
            return []
    
    def abrir_segunda_pantalla(self):
        try:
            name = self.name_entry.get()
            if not name:
                MessageBox.show_error("Error: The 'Name' field cannot be empty.")
                return
            selected_indices = self.tags_listbox.curselection()
            if not selected_indices:
                MessageBox.show_error("Error: You must select at least one tag.")
                return
            selected_tags = [self.tags_listbox.get(i) for i in selected_indices]
            tag_ids = []
            all_tags = self.get_tags()
            for tag in selected_tags:
                if tag in all_tags:
                    tag_ids.append(all_tags.index(tag) + 1)
            try:
                height = float(self.height_entry.get())
            except ValueError:
                MessageBox.show_error("Error: The 'Height' field must be an integer.")
                return
            try:
                weight = float(self.weight_entry.get())
            except ValueError:
                MessageBox.show_error("Error: The 'Weight' field must be a decimal number.")
                return
            try:
                radius_of_base = float(self.radius_of_base_entry.get())
            except ValueError:
                MessageBox.show_error("Error: The 'Radius of base' field must be a decimal number.")
                return
            material = self.material_entry.get()
            if not material:
                MessageBox.show_error("Error: The 'Material' field cannot be empty.")
                return
            main_color = self.main_color_entry.get()
            if not main_color:
                MessageBox.show_error("Error: The 'Main Color' field cannot be empty.")
                return
            secondary_color = self.secondary_color_entry.get()
            if not secondary_color:
                MessageBox.show_error("Error: The 'Secondary Color' field cannot be empty.")
                return
            shape = self.shape_entry.get()
            if not shape:
                MessageBox.show_error("Error: The 'Shape' field cannot be empty.")
                return
            bioform = self.bioform_entry.get()
            if not bioform:
                MessageBox.show_error("Error: The 'Bioform' field cannot be empty.")
                return
            
            conn = sqlite3.connect("miniatures.db")
            cursor = conn.cursor()
            cursor.execute('INSERT INTO miniature (name) VALUES (?)', (name[0]))
            conn.commit()
            miniature_id = cursor.lastrowid
            for tag_id in tag_ids:
                cursor.execute('INSERT INTO miniature_tags (miniature_id, tag_id) VALUES (?, ?)', (miniature_id, tag_id))
            conn.commit()
            cursor.execute('''
                INSERT INTO visual_metadata 
                (miniature_id, weight, height, radius_of_base, material, main_color, secondary_color, shape, bioform)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (miniature_id, weight, height, radius_of_base, material, main_color, secondary_color, shape, bioform))
            conn.commit()
            conn.close()
            
            # Cerrar la ventana actual y abrir SegundaPantalla
            self.root.destroy()
            root2 = tk.Tk()
            SegundaPantalla(root2, miniature_id, name)
            root2.mainloop()
        
        except Exception as e:
            MessageBox.show_error(f"Error inserting into database: {e}")

# -------------------- Creation Module 2 --------------------
class SegundaPantalla:
    def __init__(self, root, miniature_id, name):
        self.root = root
        self.root.title("Multi-View Dataset")
        self.miniature_id = miniature_id
        self.miniature_name = name 
        self.root.configure(bg="black")
        self.root.state('zoomed')
        
        self.segunda_frame = tk.Frame(root, bg="black")
        self.segunda_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.label = tk.Label(self.segunda_frame, text="Multi-View Dataset", bg="black", fg="white", font=("Helvetica", 20))
        self.label.pack(pady=20)
        
        self.label = tk.Label(self.segunda_frame, text="This is the second step to upload detailed information about your tiny character. None are mandatory but at least three are recommended. It is recommended to use images smaller than 7MB.", bg="black", fg="white", font=("Helvetica", 13))
        self.label.pack(pady=20)
        
        self.entry_frame = tk.Frame(self.segunda_frame, bg="black")
        self.entry_frame.pack(fill="both", expand=True)
        
        self.entry_image_info = [
            "Frontal", "Black Background", "White Background", "Lateral View 1", "Lateral View 2", "Back View",
            "Top View", "Bottom View", "Close-up View", "Isometric View", "3D Model View", "Video or GIF", "Other View"
        ]
        
        self.url_entries = {}
        self.create_entry_and_browse_widgets()
        
        self.upload_button = tk.Button(self.segunda_frame, text="Upload Images", command=self.guardar_miniature_views, bg="black", fg="white")
        self.upload_button.pack(pady=10)
        
        self.next_button = tk.Button(self.segunda_frame, text="Next Step", command=self.ir_a_tercera_pantalla, bg="black", fg="white")
        self.next_button.pack(pady=10)
    
    def create_entry_and_browse_widgets(self):
        for view_type in self.entry_image_info:
            row_frame = tk.Frame(self.entry_frame, bg="black")
            row_frame.pack(fill="x", padx=10, pady=5)
            label = tk.Label(row_frame, text=view_type, bg="black", fg="white", width=20, anchor="w")
            label.pack(side="left", padx=5)
            entry = tk.Entry(row_frame, width=50)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.url_entries[view_type] = entry
            browse_button = tk.Button(row_frame, text="Browse", command=lambda e=entry: self.browse_file(e), bg="black", fg="white")
            browse_button.pack(side="left", padx=5)
    
    def browse_file(self, entry):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)
    
    def guardar_miniature_views(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            cursor = conn.cursor()
            image_paths = {}
            for view_type, entry in self.url_entries.items():
                url = entry.get()
                if url:
                    image_paths[view_type] = url
            
            saved_image_paths = upload_photos(self.miniature_id, self.miniature_name, **image_paths)
            
            for view_type, image_filename in saved_image_paths.items():
                cursor.execute('SELECT id FROM view_types WHERE view_type = ?', (view_type,))
                result = cursor.fetchone()
                if result:
                    view_type_id = result[0]
                    cursor.execute('INSERT INTO miniature_views (miniature_id, view_type_id, url) VALUES (?, ?, ?)',
                                (self.miniature_id, view_type_id, image_filename))
            conn.commit()
            conn.close()
            MessageBox.show_info("The miniature views have been saved successfully.")
            self.limpiar_entries()
        except Exception as e:
            MessageBox.show_error(f"Error saving miniatures views:{e}")
    
    def limpiar_entries(self):
        for entry in self.url_entries.values():
            entry.delete(0, tk.END)
    
    def ir_a_tercera_pantalla(self):
        self.root.destroy()
        root3 = tk.Tk()
        TerceraPantalla(root3, self.miniature_id)
        root3.mainloop()

# -------------------- Creation Module 3 --------------------
class TerceraPantalla:
    def __init__(self, root, miniature_id):
        self.root = root
        self.root.title("Final Details")
        self.miniature_id = miniature_id
        self.root.state('zoomed')
        
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(expand=True, fill='both')
        self.tercera_frame = tk.Frame(self.main_frame, bg="black")
        self.tercera_frame.pack(expand=True)
        
        self.label = tk.Label(self.tercera_frame, text="Some Lore", font=("Helvetica", 20), bg="black", fg="white")
        self.label.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")
        
        self.alternative_text = tk.Label(self.tercera_frame, text="Finally we conclude! Just a little more information to take your collectible character into the metaverse.", font=("Helvetica", 13), bg="black", fg="white")
        self.alternative_text.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")
        
        self.designer_label = tk.Label(self.tercera_frame, text="Designer:", bg="black", fg="white")
        self.designer_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.designer_entry = tk.Entry(self.tercera_frame)
        self.designer_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        self.painted_by_label = tk.Label(self.tercera_frame, text="Painted by:", bg="black", fg="white")
        self.painted_by_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.painted_by_entry = tk.Entry(self.tercera_frame)
        self.painted_by_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        self.label_label = tk.Label(self.tercera_frame, text="Label:", bg="black", fg="white")
        self.label_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.label_entry = tk.Entry(self.tercera_frame)
        self.label_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        
        self.lore_is_canon_label = tk.Label(self.tercera_frame, text="Lore is Canon:", bg="black", fg="white")
        self.lore_is_canon_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.lore_is_canon_var = tk.StringVar(value="No")
        self.lore_frame = tk.Frame(self.tercera_frame, bg="black")
        self.lore_frame.grid(row=5, column=1, sticky="w")
        self.radio_yes = tk.Radiobutton(self.lore_frame, text="Yes", variable=self.lore_is_canon_var, value="Yes", bg="black", fg="white", selectcolor="black")
        self.radio_no = tk.Radiobutton(self.lore_frame, text="No", variable=self.lore_is_canon_var, value="No", bg="black", fg="white", selectcolor="black")
        self.radio_yes.pack(side=tk.LEFT)
        self.radio_no.pack(side=tk.LEFT)
        
        self.character_origin_label = tk.Label(self.tercera_frame, text="Character Origin:", bg="black", fg="white")
        self.character_origin_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.character_origin_entry = tk.Entry(self.tercera_frame)
        self.character_origin_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")
        
        self.story_label = tk.Label(self.tercera_frame, text="Story:", bg="black", fg="white")
        self.story_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.story_entry = tk.Entry(self.tercera_frame)
        self.story_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")
        
        self.comment_label = tk.Label(self.tercera_frame, text="Comment:", bg="black", fg="white")
        self.comment_label.grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.comment_entry = tk.Entry(self.tercera_frame)
        self.comment_entry.grid(row=8, column=1, padx=5, pady=5, sticky="ew")
        
        self.year_label = tk.Label(self.tercera_frame, text="Year:", bg="black", fg="white")
        self.year_label.grid(row=9, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = tk.Entry(self.tercera_frame)
        self.year_entry.grid(row=9, column=1, padx=5, pady=5, sticky="ew")
        
        self.reference_label = tk.Label(self.tercera_frame, text="Reference:", bg="black", fg="white")
        self.reference_label.grid(row=10, column=0, padx=5, pady=5, sticky="e")
        self.reference_entry = tk.Entry(self.tercera_frame)
        self.reference_entry.grid(row=10, column=1, padx=5, pady=5, sticky="ew")
        
        self.url_label = tk.Label(self.tercera_frame, text="URL:", bg="black", fg="white")
        self.url_label.grid(row=11, column=0, padx=5, pady=5, sticky="e")
        self.url_entry = tk.Entry(self.tercera_frame)
        self.url_entry.grid(row=11, column=1, padx=5, pady=5, sticky="ew")
        
        self.save_button = tk.Button(self.tercera_frame, text="Save & Close", command=self.guardar_datos, bg="black", fg="white")
        self.save_button.grid(row=12, column=0, columnspan=2, pady=20, padx=5)
        
        self.tercera_frame.columnconfigure(1, weight=1)
        for i in range(12):
            self.tercera_frame.rowconfigure(i, weight=1)
    
    def guardar_datos(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            cursor = conn.cursor()
            miniature_id = self.miniature_id
            designer = self.designer_entry.get()
            painted_by = self.painted_by_entry.get()
            label = self.label_entry.get()
            lore_is_canon = 1 if self.lore_is_canon_var.get() == "Yes" else 0
            character_origin = self.character_origin_entry.get()
            story = self.story_entry.get()
            comment = self.comment_entry.get()
            year = self.year_entry.get()
            reference = self.reference_entry.get()
            url = self.url_entry.get()
            
            cursor.execute('''
                INSERT INTO lore (miniature_id, designer, painted_by, label, lore_is_canon, 
                character_origin, story, comment, year, code_or_reference, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (miniature_id, designer, painted_by, label, lore_is_canon, 
                character_origin, story, comment, year, reference, url))
            
            conn.commit()
            conn.close()
            self.root.quit()
            self.root.destroy()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error saving: {str(e)}")
            
        # Mostrar mensaje de éxito
        MessageBox.show_info("Miniature created and successfully added to the database.")


# -------------------- Integración del Flujo --------------------
def main():
    # Primer paso: PantallaPrincipal
    root1 = tk.Tk()
    app1 = PantallaPrincipal(root1)
    root1.mainloop()
    # El flujo se encadena: al finalizar PantallaPrincipal se abre SegundaPantalla,
    # y al finalizar ésta se abre TerceraPantalla.
    
if __name__ == "__main__":
    main()
