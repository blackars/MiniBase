import pandas as pd
import json
import sqlite3
from message_box import MessageBox

class DataExporter:
    def __init__(self):
        pass

    def export_to_json(self, data, file_path):
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

    def export_to_excel(self, data, file_path):
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)

    def export_to_csv(self, data, file_path):
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)

    def get_all_data(self):
        try:
            conn = sqlite3.connect("miniatures.db")
            # Configurar para que las filas se devuelvan como diccionarios
            conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    m.*, v.*, l.*
                FROM 
                    miniature m
                LEFT JOIN 
                    visual_metadata v ON m.id = v.miniature_id
                LEFT JOIN 
                    lore l ON m.id = l.miniature_id
            ''')
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            MessageBox.show_error(f"Error fetching data: {e}")
            return []

    def export_to_excel_with_dialog(self, file_path):
        try:
            data = self.get_all_data()
            if data:
                self.export_to_excel(data, file_path)
                MessageBox.show_info("Data exported successfully!")
                return True
            else:
                MessageBox.show_warning("No data to export!")
                return False
        except Exception as e:
            MessageBox.show_error(f"Error exporting data: {e}")
            return False

    def export_to_csv_with_dialog(self, file_path):
        try:
            data = self.get_all_data()
            if data:
                self.export_to_csv(data, file_path)
                MessageBox.show_info("Data exported successfully!")
                return True
            else:
                MessageBox.show_warning("No data to export!")
                return False
        except Exception as e:
            MessageBox.show_error(f"Error exporting data: {e}")
            return False

    def export_to_json_with_dialog(self, file_path):
        try:
            data = self.get_all_data()
            if data:
                self.export_to_json(data, file_path)
                MessageBox.show_info("Data exported successfully!")
                return True
            else:
                MessageBox.show_warning("No data to export!")
                return False
        except Exception as e:
            MessageBox.show_error(f"Error exporting data: {e}")
            return False
