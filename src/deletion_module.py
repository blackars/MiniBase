import os
import sqlite3
import shutil
from message_box import MessageBox

def delete_mini(mini_path):
    """
    Elimina un archivo de miniatura después de mostrar un cuadro de confirmación.
    
    Args:
        mini_path (str): Ruta completa del archivo a eliminar.
    
    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    if not os.path.exists(mini_path):
        MessageBox.show_error("The mini does not exist.")
        return False

    # Mostrar cuadro de confirmación usando MessageBox personalizado
    confirm = MessageBox.ask_confirmation(
        "Are you sure you want to permanently delete this mini?"
    )

    if confirm:
        try:
            os.remove(mini_path)
            MessageBox.show_info("Mini deleted successfully.")
            return True
        except Exception as e:
            MessageBox.show_error(f"Failed to delete the mini: {str(e)}")
            return False

    return False

def delete_miniature(miniature_id, miniature_name):
    """
    Elimina una miniatura y todos sus datos relacionados de la base de datos y del sistema de archivos.
    """
    conn = None
    try:
        # Establecer conexión con la base de datos SQLite
        conn = sqlite3.connect("miniatures.db")
        cursor = conn.cursor()

        # Mostrar confirmación antes de proceder
        confirm = MessageBox.ask_confirmation(
            f"Are you sure you want to permanently delete the mini '{miniature_name}'?"
        )
        if not confirm:
            return False

        # Realizar operaciones de eliminación en la base de datos
        cursor.execute("DELETE FROM lore WHERE miniature_id = ?", (miniature_id,))
        cursor.execute("DELETE FROM visual_metadata WHERE miniature_id = ?", (miniature_id,))
        cursor.execute("DELETE FROM miniature_tags WHERE miniature_id = ?", (miniature_id,))
        cursor.execute("DELETE FROM miniature WHERE id = ?", (miniature_id,))
        conn.commit()

        # Eliminar la carpeta de imágenes asociada
        images_folder = f"images/{miniature_id}_{miniature_name}"
        if os.path.exists(images_folder):
            shutil.rmtree(images_folder)

        MessageBox.show_info("Mini deleted successfully")
        return True

    except Exception as e:
        MessageBox.show_error(f"Failed to delete the mini: {str(e)}")
        if conn:
            conn.rollback()
        return False

    finally:
        if conn:
            conn.close()
