import os
import shutil

def upload_photos(miniature_id, miniature_name, **kwargs):
    miniature_folder = f"images/{miniature_id}_{miniature_name}"
    os.makedirs(miniature_folder, exist_ok=True)

    image_paths = {}
    for key, path in kwargs.items():
        if path:
            image_name = os.path.basename(path)
            new_path = os.path.join(miniature_folder, image_name)
            shutil.copy(path, new_path)
            image_paths[key] = new_path

    return image_paths

