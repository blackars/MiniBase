import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SchemaView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Schema View - Browse Data")
        self.configure(bg="black")
        self.geometry("800x600")
        self.create_widgets()
        self.load_table_names()
        
    def create_widgets(self):
        # Creamos un estilo local usando nombres de estilo únicos.
        self.local_style = ttk.Style(self)
        # Copiamos el layout del encabezado por defecto a nuestro estilo personalizado
        heading_layout = self.local_style.layout("Treeview.Heading")
        self.local_style.layout("SchemaView.Treeview.Heading", heading_layout)
        
        # Configuración de estilos personalizados para esta ventana
        self.local_style.configure("SchemaView.Treeview",
                                    background="black",
                                    foreground="white",
                                    fieldbackground="black",
                                    font=("Helvetica", 10))
        self.local_style.map("SchemaView.Treeview", background=[('selected', '#666666')])
        
        self.local_style.configure("SchemaView.Treeview.Heading",
                                    background="black",
                                    foreground="black",
                                    font=("Helvetica", 11, "bold"))
        self.local_style.map("SchemaView.Treeview.Heading",
                            background=[('active', 'black')],
                            foreground=[('active', 'white')])
        
        # Forzar el layout de la treearea para que ocupe todo el widget usando el fieldbackground
        self.local_style.layout("SchemaView.Treeview", 
            [('Treeview.treearea', {'sticky': 'nswe'})]
        )
        
        # Frame superior para seleccionar tabla y refrescar
        top_frame = tk.Frame(self, bg="black")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        lbl = tk.Label(top_frame, text="Select Table:", bg="black", fg="white", font=("Helvetica", 13))
        lbl.pack(side=tk.LEFT, padx=(0,5))
        
        self.table_combo = ttk.Combobox(top_frame, state="readonly")
        self.table_combo.pack(side=tk.LEFT, padx=(0,5))
        self.table_combo.bind("<<ComboboxSelected>>", self.on_table_select)
        
        refresh_btn = tk.Button(top_frame, text="Refresh", bg="black", fg="white", font=("Helvetica", 13),
                                command=self.load_table_names)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Frame para mostrar los datos en formato sheet
        tree_frame = tk.Frame(self, bg="black")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Creamos el Treeview usando estilos personalizados.
        self.tree = ttk.Treeview(tree_frame, show="headings", style="SchemaView.Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vsb.set)

    def load_table_names(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            cursor = conn.cursor()
            # Obtener todas las tablas de usuario (excluyendo las internas)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            self.table_combo['values'] = tables
            if tables:
                self.table_combo.current(0)
                self.load_table_data(tables[0])
        except Exception as e:
            messagebox.showerror("Error", f"Error loading table names: {e}")
    
    def on_table_select(self, event):
        table_name = self.table_combo.get()
        self.load_table_data(table_name)
    
    def load_table_data(self, table_name):
        try:
            conn = sqlite3.connect("miniatures.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            conn.close()
            
            columns = rows[0].keys() if rows else []
            # Limpiar el Treeview actual
            self.tree.delete(*self.tree.get_children())
            self.tree['columns'] = columns
            
            # Configurar encabezados y columnas usando el estilo personalizado
            for col in columns:
                # Añadimos un comando en el encabezado para ordenar por esa columna
                self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))
                self.tree.column(col, anchor="center", stretch=True)
            
            # Insertar cada fila en el Treeview
            for row in rows:
                values = [row[col] for col in columns]
                self.tree.insert("", tk.END, values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading table data for {table_name}: {e}")
    
    def sort_column(self, col, reverse):
        """Ordena las filas del Treeview por la columna 'col' en orden ascendente o descendente."""
        try:
            # Obtener los elementos actuales del Treeview y sus valores en la columna 'col'
            l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
            # Intentar convertir los valores a float para orden numérico, si falla se ordena como string
            try:
                l.sort(key=lambda t: float(t[0]) if t[0] != "" else float('-inf'), reverse=reverse)
            except ValueError:
                l.sort(key=lambda t: t[0].lower(), reverse=reverse)
            
            # Reorganizar los elementos según el orden obtenido
            for index, (val, k) in enumerate(l):
                self.tree.move(k, '', index)
            
            # Cambiar el comando del encabezado para invertir el orden en la siguiente pulsación
            self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
        except Exception as e:
            messagebox.showerror("Error", f"Error sorting column {col}: {e}")
