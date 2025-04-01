# User Manual & Technical Documentation

This manual details the functionalities of **MiniBase**, providing clear instructions on how to use each module of the application. The documentation is designed so that, through the "Info" button in the app, users can interactively learn about each feature.

## Application Usage

### **Creating Miniatures**
1. Open the application  
2. Select **"Add New Mini"**  
3. Fill in the basic details and select tags  
4. Upload images of the miniature  
5. Add narrative information and lore  
6. Save the miniature  

### **Editing Miniatures**
1. Select the miniature to edit  
2. Click **"Edit Mini"**  
3. Modify the necessary fields  
4. Update images if needed  
5. Save changes using **"Save & Close"**  

### **Deleting Miniatures**
1. Select the miniature to delete  
2. Click **"Delete Mini"**  
3. Confirm the deletion  
4. The miniature and all its associated data will be permanently removed  

### **Import/Export**
1. Select the desired operation  
2. Choose the file format  
3. Select the data to import/export  
4. Confirm the operation  

## Key Features of the Application

### **Miniature Management**
- Create new miniatures with detailed attributes  
- Edit existing miniatures  
- Delete miniatures and their associated data  
- View detailed information on each miniature  

### **Visual Metadata**
- Weight and dimensions  
- Materials and colors  
- Shape and bioform  
- Multiple photographic or custom image views:
  - Front View  
  - Black Background  
  - White Background  
  - Lateral View 1  
  - Lateral View 2  
  - Back View  
  - Top View  
  - Bottom View  
  - Close-up View  
  - Isometric View  
  - 3D Model View  
  - Video or GIF  
  - Other View  

### **Tag System**
- Predefined and customizable tags  
- Multiple tags per miniature  
- Categorized organization  

### **Lore Management**
- Designer information  
- Painter details  
- Narrative tags  
- Is the added lore canon?  
- Character origin  
- Story and comments  
- Year and references  
- External links  

### **Import & Export**
- **Excel Import** using the following structure:
  - `template.xlsx`  
- **Export to multiple formats:**
  - JSON  
  - Excel  
  - CSV  

## System Requirements

### **Required Software**
- Python 3.11 or later  
- SQLite3 (included in Python)  

### **Python Dependencies**
```bash
tkinter
sqlite3
pandas
Pillow
```


  1. Clone the repositorio:
  ```bash
  git clone https://github.com/blackars/MiniBase.git
  cd MiniBase
  ```

  2. Install the dependencies:
  ```bash
  pip install pandas Pillow
  ```

  3. Run the application:
  ```bash
  python src/gui_app.py
  ```

  ## Project Structure

  ```
  MiniBase/
  ├──screenshots/
  ├── src/
  |   ├── images/
  │   ├── gui_app.py
  │   ├── home_screen.py
  │   ├── creation_module.py
  │   ├── edition_module.py
  │   ├── deletion_module.py
  │   ├── importation_module.py
  │   ├── exportation_module.py
  │   ├── schemaview_module.py
  │   ├── photo_uploader.py
  │   ├── message_box.py
  │   ├── info_window.py
  │   ├── initialize_db.py
  │   ├── schema.sql
  │   ├── miniatures.db
  │   ├── MiniBase_Logo.ico
  │   ├── MiniBase_Logo.png
  │   └── TECHNOLOGY.md
  ├── LICENSE
  ├── requirements.txt
  ├── README.md
  └── template.xlsx
  ```


  ## Contributions

  Contributions are welcome. Please follow these steps:


  1. Fork the repository.

  2. Create a branch for your feature: 
  ```bash
  git checkout -b feature/AmazingFeature
  ```
  3. Commit your changes:
  ```bash 
    git commit -m 'Add some AmazingFeature'
  ```
  4. Push the branch: 
  ```bash
    git push origin feature/AmazingFeature`)
  ```
  
  5. Open a Pull Request and briefly describe the changes made to facilitate review.


  ## Licencia

  Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

  ## Contacto

  Brayan Andres Castillo Mesa @blackars - [@_arsblack_](https://twitter.com/arsblack) - 

  Link del Proyecto: [https://github.com/blackars/MiniBase](https://github.com/blackars/MiniBase) 