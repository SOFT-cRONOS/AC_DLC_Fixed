import os
import webbrowser
import pathlib
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# Traducciones
translations = {
    "en": {
        "title": "Assetto Corsa DLC Fixed",
        "select_folder": "Select the Assetto Corsa root folder:",
        "browse": "Browse",
        "scan": "Scan",
        "run_fixed": "Run Fixed",
        "processing": "Processing folders...\n",
        "done": "Done! Processed folders:\n",
        "success": "The collider files have been successfully created.",
        "error": "Error",
        "folder_missing": "The file 'collider.kn5' was not found in the same directory as this script.",
        "select_folder_error": "Please select the Assetto Corsa CONTENT folder.",
        "select_language": "Select Language: Español",
        "about": "About this application:\nThis app allows you to fix \nAssetto Corsa DLCs by replacing\n missing collider files.",
        "atention": "Use at your own risk",
    },
    "es": {
        "title": "Reparador de DLC de Assetto Corsa",
        "select_folder": "Selecciona la carpeta raíz de Assetto Corsa:",
        "browse": "Explorar",
        "scan": "Escanear",
        "run_fixed": "Ejecutar Reparacion",
        "processing": "Procesando carpetas...\n",
        "done": "¡Hecho! Carpetas procesadas:\n",
        "success": "Los archivos collider se han creado con éxito.",
        "error": "Error",
        "folder_missing": "El archivo 'collider.kn5' no se encontró en el mismo directorio que este script.",
        "select_folder_error": "Por favor, selecciona la carpeta CONTENT de Assetto Corsa.",
        "select_language": "Seleccionar Idioma: English",
        "about": "Acerca de esta aplicación:\nEsta aplicación permite reparar los DLCs de \nAssetto Corsa reemplazando archivos\n collider faltantes.",
        "atention": "Uso a responsabilidad del usuario",
    }
}

# Idioma actual
current_language = "en"

# Colores para tema oscuro
dark_theme = {
    "bg": "#2b2b2b",
    "fg": "#f5f5f5",
    "button_bg": "#3c3f41",
    "button_fg": "#ffffff",
    "entry_bg": "#3c3f41",
    "entry_fg": "#ffffff",
    "text_bg": "#1e1e1e",
    "text_fg": "#f5f5f5",
}

def process_folders(root_path, collider_path, selected_folders):
    try:
        cars_folder = pathlib.Path(root_path) / "content/cars"
        if not cars_folder.exists() or not cars_folder.is_dir():
            raise FileNotFoundError(f"The folder 'cars' does not exist in the specified path: {root_path}")

        with open(collider_path, "rb") as f:
            collider_data = f.read()

        processed_folders = []

        for folder in selected_folders:
            folder_path = cars_folder / folder
            collider_file_path = folder_path / "collider.kn5"
            backup_collider_path = folder_path / "bkp_collider.kn5"

            # Verificar si el archivo collider.kn5 existe y renombrarlo a bkp_collider.kn5
            if collider_file_path.exists():
                collider_file_path.rename(backup_collider_path)

            # Copiar el nuevo archivo collider.kn5
            with open(collider_file_path, "wb") as collider_file:
                collider_file.write(collider_data)
            
            processed_folders.append(folder)

        return processed_folders

    except Exception as e:
        messagebox.showerror(translations[current_language]["error"], f"An error occurred: {e}")
        return None

def select_root_folder(entry_widget):
    folder_selected = filedialog.askdirectory(title=translations[current_language]["select_folder"])
    if folder_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)

def scan_folders(entry_root, listbox):
    root_path = entry_root.get().strip()
    if not root_path:
        messagebox.showerror(translations[current_language]["error"], translations[current_language]["select_folder_error"])
        return

    cars_folder = pathlib.Path(root_path) / "content/cars"
    if not cars_folder.exists() or not cars_folder.is_dir():
        messagebox.showerror(translations[current_language]["error"], f"The folder 'cars' does not exist in the specified path: {root_path}")
        return

    listbox.delete(0, tk.END)
    folders = sorted([f.name for f in cars_folder.iterdir() if f.is_dir()])  # Orden alfabético
    for folder in folders:
        listbox.insert(tk.END, folder)

def run_fixed(entry_root, listbox, text_output):
    root_path = entry_root.get().strip()
    if not root_path:
        messagebox.showerror(translations[current_language]["error"], translations[current_language]["select_folder_error"])
        return

    collider_path = pathlib.Path(sys.argv[0]).parent / "collider.kn5"
    if not collider_path.exists():
        messagebox.showerror(translations[current_language]["error"], translations[current_language]["folder_missing"])
        return

    selected_folders = [listbox.get(i) for i in listbox.curselection()]  # Solo carpetas seleccionadas
    if not selected_folders:
        messagebox.showerror(translations[current_language]["error"], "No folders selected.")
        return

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, translations[current_language]["processing"])
    processed_folders = process_folders(root_path, collider_path, selected_folders)

    if processed_folders is not None:
        text_output.insert(tk.END, translations[current_language]["done"])
        for folder in processed_folders:
            text_output.insert(tk.END, f"- {folder}\n")
        messagebox.showinfo(translations[current_language]["success"], translations[current_language]["success"])

def toggle_language(language_button, labels):
    global current_language
    current_language = "es" if current_language == "en" else "en"
    update_labels(labels)
    language_button.config(text=translations[current_language]["select_language"])

def update_labels(labels):
    labels["title"].config(text=translations[current_language]["title"])
    labels["select_folder"].config(text=translations[current_language]["select_folder"])
    labels["scan_button"].config(text=translations[current_language]["scan"])
    labels["run_button"].config(text=translations[current_language]["run_fixed"])

def show_about():
    about_window = tk.Toplevel()
    about_window.title(translations[current_language]["title"])
    about_window.geometry("400x300")
    about_window.config(bg=dark_theme["bg"])

    # Texto de descripción
    label_about = tk.Label(
        about_window, 
        text=translations[current_language]["about"], 
        font=("Arial", 12), 
        bg=dark_theme["bg"], 
        fg=dark_theme["fg"]
    )
    label_about.pack(pady=10)

    # Enlace con "Más info aquí"
    def open_link(event):
        webbrowser.open("https://www.softcronos.com.ar")  # Cambia el enlace por el que desees

    link_label = tk.Label(
        about_window,
        text="Más info aquí",
        font=("Arial", 12, "underline"),  # Subrayado para parecer un enlace
        bg=dark_theme["bg"],
        fg="blue",  # Color azul para indicar que es un enlace
        cursor="hand2"  # Cambia el cursor al pasar sobre el texto
    )
    link_label.pack(pady=5)
    link_label.bind("<Button-1>", open_link)  # Asocia el evento de clic con la función `open_link`

    # Botón para cerrar la ventana
    button_close = tk.Button(
        about_window, 
        text="Close", 
        command=about_window.destroy, 
        bg=dark_theme["button_bg"], 
        fg=dark_theme["button_fg"]
    )
    button_close.pack(pady=10)

def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title(translations[current_language]["title"])
    root.geometry("600x700")
    root.config(bg=dark_theme["bg"])
    
    # Etiqueta de introducción
    labels = {}
    labels["title"] = tk.Label(root, text=translations[current_language]["title"], font=("Arial", 16), bg=dark_theme["bg"], fg=dark_theme["fg"])
    labels["title"].pack(pady=10)
    labels["select_folder"] = tk.Label(root, text=translations[current_language]["select_folder"], font=("Arial", 12), bg=dark_theme["bg"], fg=dark_theme["fg"])
    labels["select_folder"].pack(pady=5)
    
    # Campo de entrada para la ruta raíz
    frame_path = tk.Frame(root, bg=dark_theme["bg"])
    frame_path.pack(pady=5)
    entry_root = tk.Entry(frame_path, width=50, bg=dark_theme["entry_bg"], fg=dark_theme["entry_fg"], insertbackground=dark_theme["fg"])
    entry_root.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_path, text=translations[current_language]["browse"], command=lambda: select_root_folder(entry_root),
              bg=dark_theme["button_bg"], fg=dark_theme["button_fg"], activebackground=dark_theme["entry_bg"]).pack(side=tk.LEFT, padx=5)
    
    # Botón para escanear carpetas
    labels["scan_button"] = tk.Button(root, text=translations[current_language]["scan"], command=lambda: scan_folders(entry_root, listbox),
                                     bg=dark_theme["button_bg"], fg=dark_theme["button_fg"], activebackground=dark_theme["entry_bg"])
    labels["scan_button"].pack(pady=10)
    
    # Lista de carpetas
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, bg=dark_theme["entry_bg"], fg=dark_theme["entry_fg"], selectbackground=dark_theme["button_bg"])
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)
    
    # Botón para ejecutar el fixed
    labels["run_button"] = tk.Button(root, text=translations[current_language]["run_fixed"], command=lambda: run_fixed(entry_root, listbox, text_output),
                                     bg=dark_theme["button_bg"], fg=dark_theme["button_fg"], activebackground=dark_theme["entry_bg"])
    labels["run_button"].pack(pady=10)
    
    # Botón para cambiar idioma
    language_button = tk.Button(root, text=translations[current_language]["select_language"], command=lambda: toggle_language(language_button, labels),
                                 bg=dark_theme["button_bg"], fg=dark_theme["button_fg"], activebackground=dark_theme["entry_bg"])
    language_button.pack(pady=10)
    
    # Cuadro de texto para mostrar resultados
    text_output = tk.Text(root, width=70, height=15, state=tk.NORMAL, bg=dark_theme["text_bg"], fg=dark_theme["text_fg"], insertbackground=dark_theme["fg"])
    text_output.pack(pady=10)
    
    # Botón de "Acerca de"
    button_about = tk.Button(root, text="?", command=show_about, bg=dark_theme["button_bg"], fg=dark_theme["button_fg"])
    button_about.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-50)

    # Texto en la parte inferior derecha
    label_disclaimer = tk.Label(root, text=translations[current_language]["atention"], font=("Arial", 8), bg=dark_theme["bg"], fg=dark_theme["fg"])
    label_disclaimer.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    # Iniciar el bucle de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()