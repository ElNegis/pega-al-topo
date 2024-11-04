import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

class TaekwondoUserManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios - Sistema de Taekwondo")
        self.root.geometry("800x600")
        
        # Configuración de la base de datos
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'BD_Taekwondo'
        }
        
        # Variables para los campos
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellidos_var = tk.StringVar()
        
        self.setup_ui()
        self.load_users()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sección de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Usuario", padding="10")
        form_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Campos del formulario
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.id_var, state='readonly').grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.nombre_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Apellidos:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(form_frame, textvariable=self.apellidos_var).grid(row=2, column=1, padx=5, pady=5)
        
        # Botones de acción
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Nuevo", command=self.new_user).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Guardar", command=self.save_user).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.delete_user).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_form).grid(row=0, column=3, padx=5)
        
        # Tabla de usuarios
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Usuarios", padding="10")
        table_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar la tabla
        columns = ('ID', 'Nombre', 'Apellidos', 'Fecha Registro')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Configurar las columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        # Scrollbars
        yscrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        xscrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        
        # Ubicar elementos
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        yscrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        xscrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Configurar expansión
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
    def db_connect(self):
        """Establece conexión con la base de datos"""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
            return None
            
    def load_users(self):
        """Carga los usuarios en la tabla"""
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = self.db_connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuarios ORDER BY id_usuario")
                
                for user in cursor.fetchall():
                    # Formatear la fecha
                    fecha = user[3].strftime('%Y-%m-%d %H:%M:%S') if user[3] else ''
                    self.tree.insert('', tk.END, values=(user[0], user[1], user[2], fecha))
                    
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al cargar usuarios: {err}")
            finally:
                conn.close()
                
    def clear_form(self):
        """Limpia el formulario"""
        self.id_var.set('')
        self.nombre_var.set('')
        self.apellidos_var.set('')
        
    def new_user(self):
        """Prepara el formulario para un nuevo usuario"""
        self.clear_form()
        
    def save_user(self):
        """Guarda o actualiza un usuario"""
        nombre = self.nombre_var.get().strip()
        apellidos = self.apellidos_var.get().strip()
        
        if not nombre or not apellidos:
            messagebox.showwarning("Datos Incompletos", "Por favor complete todos los campos")
            return
            
        conn = self.db_connect()
        if conn:
            try:
                cursor = conn.cursor()
                user_id = self.id_var.get()
                
                if user_id:  # Actualizar
                    cursor.execute("""
                        UPDATE usuarios 
                        SET nombre = %s, apellidos = %s 
                        WHERE id_usuario = %s
                    """, (nombre, apellidos, user_id))
                    messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                else:  # Insertar nuevo
                    cursor.execute("""
                        INSERT INTO usuarios (nombre, apellidos) 
                        VALUES (%s, %s)
                    """, (nombre, apellidos))
                    messagebox.showinfo("Éxito", "Usuario creado correctamente")
                
                conn.commit()
                self.load_users()
                self.clear_form()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al guardar usuario: {err}")
            finally:
                conn.close()
                
    def delete_user(self):
        """Elimina un usuario"""
        user_id = self.id_var.get()
        if not user_id:
            messagebox.showwarning("Selección Requerida", "Por favor seleccione un usuario para eliminar")
            return
            
        if not messagebox.askyesno("Confirmar Eliminación", 
                                  "¿Está seguro de que desea eliminar este usuario?\n" +
                                  "Esta acción no se puede deshacer."):
            return
            
        conn = self.db_connect()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (user_id,))
                conn.commit()
                
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.load_users()
                self.clear_form()
                
            except mysql.connector.Error as err:
                if err.errno == 1451:  # Error de clave foránea
                    messagebox.showerror("Error", 
                        "No se puede eliminar este usuario porque tiene sesiones registradas")
                else:
                    messagebox.showerror("Error", f"Error al eliminar usuario: {err}")
            finally:
                conn.close()
                
    def on_select(self, event):
        """Maneja la selección de un usuario en la tabla"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            user = item['values']
            
            self.id_var.set(user[0])
            self.nombre_var.set(user[1])
            self.apellidos_var.set(user[2])

if __name__ == '__main__':
    root = tk.Tk()
    app = TaekwondoUserManager(root)
    root.mainloop()
