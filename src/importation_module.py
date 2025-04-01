import pandas as pd
import sqlite3
from message_box import MessageBox
import json
import time

class DataImporter:
    @staticmethod
    def get_tag_mapping(cursor):
        # Consulta utilizando los nombres de columnas de la tabla 'tags'
        cursor.execute('SELECT id, tag FROM tags')
        tags = cursor.fetchall()
        return {tag[1]: tag[0] for tag in tags}  # { "tag_name": id, ... }

    @staticmethod
    def safe_value(val):
        """
        Convierte valores 'nan', 'NaN', cadenas vacías, etc., a None
        para que en SQLite se inserten como NULL.
        """
        if val is None:
            return None
        val_str = str(val).strip()
        if not val_str or val_str.lower() in ['nan', 'none']:
            return None
        return val

    @staticmethod
    def import_data():
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            try:
                # Leer Excel con opciones específicas
                df = pd.read_excel(
                    file_path,
                    engine='openpyxl',
                    dtype=str  # Tratar todas las columnas como texto inicialmente
                )
                #print("Columnas encontradas en el Excel:", df.columns.tolist())
                #print("Primeras filas del Excel:")
                #print(df.head())
                
                # Convertir a registros (diccionarios) para procesar
                data = df.to_dict(orient='records')
                #print("\nPrimer registro convertido:")
                #if data:
                #    print(json.dumps(data[0], indent=2))
                
                if data:
                    DataImporter.load_data_into_db(data)
                    MessageBox.show_info("Data imported successfully.")
                else:
                    MessageBox.show_error("The Excel file is empty or does not have valid data.")
            except Exception as e:
                MessageBox.show_error(f"Error al importar los datos: {e}")
                print(f"Error detallado: {str(e)}")
                import traceback
                print(traceback.format_exc())

    @staticmethod
    def load_data_into_db(data):
        try:
            # Conexión con timeout elevado (30 segundos)
            conn = sqlite3.connect("miniatures.db", timeout=30)
            cursor = conn.cursor()
            
            # Obtener el mapeo de tags al inicio
            tag_mapping = DataImporter.get_tag_mapping(cursor)
            
            for record in data:
                name = DataImporter.safe_value(record.get('name'))
                attempts = 0
                while attempts < 5:
                    try:
                        # Insertar en 'miniature'
                        insert_miniature_sql = """
                            INSERT INTO miniature (name)
                            VALUES (?)
                        """
                        cursor.execute(insert_miniature_sql, (name,))
                        miniature_id = cursor.lastrowid
                        
                        # Insertar en 'visual_metadata'
                        insert_visual_sql = """
                            INSERT INTO visual_metadata 
                            (miniature_id, main_color, secondary_color, shape, bioform, material, weight, height, radius_of_base)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        cursor.execute(insert_visual_sql, (
                            miniature_id,
                            DataImporter.safe_value(record.get('main_color')),
                            DataImporter.safe_value(record.get('secondary_color')),
                            DataImporter.safe_value(record.get('shape')),
                            DataImporter.safe_value(record.get('bioform')),
                            DataImporter.safe_value(record.get('material')),
                            DataImporter.safe_value(record.get('weight')),
                            DataImporter.safe_value(record.get('height')),
                            DataImporter.safe_value(record.get('radius_of_base'))
                        ))
                        
                        # Obtener el valor del campo 'tags' del registro
                        tag_string = DataImporter.safe_value(record.get('tags'))
                        if tag_string:
                            # Separar los tags en caso de haber más de uno (asumiendo que se separan por comas)
                            tag_list = [t.strip() for t in tag_string.split(',') if t.strip()]
                            if tag_list:
                                for tag_name in tag_list:
                                    # Buscar el id del tag usando el mapeo obtenido previamente
                                    tag_id = tag_mapping.get(tag_name)
                                    if tag_id:
                                        # Insertar en la tabla de relación
                                        insert_tag_sql = """
                                            INSERT INTO miniature_tags (miniature_id, tag_id)
                                            VALUES (?, ?)
                                        """
                                        cursor.execute(insert_tag_sql, (miniature_id, tag_id))
                                    else:
                                        print(f"Warning: Tag '{tag_name}' no encontrado en la base de datos")
                        
                        # Insertar en 'lore'
                        insert_lore_sql = """
                            INSERT INTO lore
                            (miniature_id, designer, painted_by, label, lore_is_canon, 
                            character_origin, story, comment, year, code_or_reference, url)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        cursor.execute(insert_lore_sql, (
                            miniature_id,
                            DataImporter.safe_value(record.get('designer')),
                            DataImporter.safe_value(record.get('painted_by')),
                            DataImporter.safe_value(record.get('label')),
                            DataImporter.safe_value(record.get('lore_is_canon')),
                            DataImporter.safe_value(record.get('character_origin')),
                            DataImporter.safe_value(record.get('story')),
                            DataImporter.safe_value(record.get('comment')),
                            DataImporter.safe_value(record.get('year')),
                            DataImporter.safe_value(record.get('code_or_reference')),
                            DataImporter.safe_value(record.get('URL'))
                        ))
                        
                        conn.commit()
                        break  # Salir del bucle de reintentos si todo funcionó
                    except sqlite3.OperationalError as op_err:
                        if "database is locked" in str(op_err).lower():
                            attempts += 1
                            print(f"Database locked. Retrying {attempts}/5 for registration '{name}'...")
                            time.sleep(1)
                        else:
                            print(f"Record-specific SQL error '{name}': {op_err}")
                            conn.rollback()
                            break
                    except Exception as e:
                        print(f"Record-specific SQL error '{name}': {e}")
                        conn.rollback()
                        break
                    
            conn.close()
            
        except Exception as e:
            print(f"General error: {e}")
            if 'conn' in locals():
                conn.close()
            raise
