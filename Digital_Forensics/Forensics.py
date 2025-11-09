import os
import csv
import pprint
import logging
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Set up logging
logging.basicConfig(filename="errors.log", level=logging.WARNING)

# Extract file metadata
def extract_metadata(file_path):
    try:
        file_path = Path(file_path).resolve(strict=True)
        file_stats = file_path.stat()
        metadata = {
            "File Name": file_path.name,
            "File Type": file_path.suffix,
            "File Size (bytes)": file_stats.st_size,
            "Creation Time": datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            "Last Modified Time": datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "Last Accessed Time": datetime.fromtimestamp(file_stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
        }
        return metadata
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}")
        return {"Error": f"File not found: {file_path}"}
    except Exception as e:
        logging.warning(f"Error with {file_path}: {e}")
        return {"Error": f"An error occurred for {file_path}: {str(e)}"}

# GUI Application Class
class MetadataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Metadata Extractor")
        self.root.geometry("800x600")
        self.metadata_list = []

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.create_widgets()

    def create_widgets(self):
        # Menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Select Files", command=self.browse_files)
        file_menu.add_command(label="Clear Output", command=self.clear_output)
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Select Files", command=self.browse_files).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Clear Output", command=self.clear_output).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).grid(row=0, column=2, padx=5)

        # Output
        self.output_box = tk.Text(self.root, wrap=tk.WORD, font=('Consolas', 10))
        self.output_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select one or more files",
            filetypes=[("All files", "*.*"), ("Text files", "*.txt"), ("CSV files", "*.csv")]
        )
        if not file_paths:
            return
        self.display_metadata(file_paths)

    def display_metadata(self, file_paths):
        self.clear_output()
        self.metadata_list = []
        for path in file_paths:
            metadata = extract_metadata(path)
            if "Error" not in metadata:
                self.metadata_list.append(metadata)
            self.output_box.insert(tk.END, pprint.pformat(metadata) + "\n\n")
        self.status_bar.config(text=f"Loaded {len(file_paths)} file(s)")

    def clear_output(self):
        self.output_box.delete(1.0, tk.END)
        self.status_bar.config(text="Output cleared")
        self.metadata_list = []

    def export_to_csv(self):
        if not self.metadata_list:
            messagebox.showwarning("No Data", "No metadata to export.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save metadata as CSV")
        if not save_path:
            return

        try:
            with open(save_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.metadata_list[0].keys())
                writer.writeheader()
                writer.writerows(self.metadata_list)
            self.status_bar.config(text=f"Metadata exported to {save_path}")
        except Exception as e:
            logging.error(f"Export error: {e}")
            messagebox.showerror("Export Failed", f"Failed to export metadata: {str(e)}")

    def show_about(self):
        messagebox.showinfo("About", "File Metadata Extractor\nCreated with Python and tkinter.\n\nSelect files to view detailed metadata.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataApp(root)
    root.mainloop()