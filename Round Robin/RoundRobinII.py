import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Aquí puedes añadir el código para obtener las rutas de los archivos
import os
import sys

# Obtener la ruta del directorio donde se encuentra el ejecutable
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Ejecutándose como un ejecutable
else:
    base_path = os.path.dirname(__file__)  # Ejecutándose en un entorno normal

# Construir rutas a los archivos de la carpeta images
logo_jpg_path = os.path.join(base_path, 'images', 'tu_logo.jpg')
logo_ico_path = os.path.join(base_path, 'images', 'tu_logo.ico')

class RoundRobinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Round Robin Simplificado")
        self.root.geometry("800x600")
        
        # Establecer el ícono de la ventana
        self.root.iconbitmap("images/tu_logo.ico")  # Cambia esto a la ruta de tu icono

        # Cambiar colores
        self.root.configure(bg="#010132")  # Color de fondo de la ventana

        # Logo
        self.logo_image = Image.open("images/tu_logo.jpg")  # Cambia esto a la ruta de tu logo
        self.logo_image = self.logo_image.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar si es necesario
        self.logo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(root, image=self.logo, bg="#010132")
        self.logo_label.pack(pady=10)

        # Lista de procesos y tiempos de CPU
        self.process_list = []
        self.burst_times = []

       # Etiquetas para promedios
        self.lbl_avg_waiting = tk.Label(root, text="Tiempo promedio de espera: N/A", bg="#010132", fg="white")
        self.lbl_avg_waiting.pack(pady=5)

        self.lbl_avg_turnaround = tk.Label(root, text="Tiempo promedio de retorno: N/A", bg="#010132", fg="white")
        self.lbl_avg_turnaround.pack(pady=5)

        # Etiquetas e inputs para añadir procesos
        self.lbl_proceso = tk.Label(root, text="Añadir nuevo proceso", bg="#010132", fg="white")
        self.lbl_proceso.pack(pady=5)

        self.lbl_tiempo_cpu = tk.Label(root, text="Tiempo en CPU:", bg="#010132", fg="white")
        self.lbl_tiempo_cpu.pack()
        self.txt_tiempo_cpu = tk.Entry(root)
        self.txt_tiempo_cpu.pack(pady=5)

        # Botón para añadir procesos
        self.btn_add_proceso = tk.Button(root, text="Añadir Proceso +", command=self.add_process, bg="#FF00FF", fg="white")
        self.btn_add_proceso.pack(pady=5)
        self.btn_add_proceso.bind("<Enter>", lambda e: self.on_enter(e, self.btn_add_proceso))
        self.btn_add_proceso.bind("<Leave>", lambda e: self.on_leave(e, self.btn_add_proceso))

        # Tabla para mostrar procesos añadidos
        self.tree = ttk.Treeview(root, columns=("Proceso", "Tiempo de CPU"), show="headings", height=5)
        self.tree.heading("Proceso", text="Proceso")
        self.tree.heading("Tiempo de CPU", text="Tiempo de CPU")
        self.tree.pack(pady=5)

        # Botones para editar y borrar procesos
        self.btn_edit_proceso = tk.Button(root, text="Editar Proceso", command=self.edit_process, bg="#FF00FF", fg="white")
        self.btn_edit_proceso.pack(pady=5)
        self.btn_edit_proceso.bind("<Enter>", lambda e: self.on_enter(e, self.btn_edit_proceso))
        self.btn_edit_proceso.bind("<Leave>", lambda e: self.on_leave(e, self.btn_edit_proceso))

        self.btn_delete_proceso = tk.Button(root, text="Borrar Proceso", command=self.delete_process, bg="#FF00FF", fg="white")
        self.btn_delete_proceso.pack(pady=5)
        self.btn_delete_proceso.bind("<Enter>", lambda e: self.on_enter(e, self.btn_delete_proceso))
        self.btn_delete_proceso.bind("<Leave>", lambda e: self.on_leave(e, self.btn_delete_proceso))

        # Botón para ejecutar el algoritmo
        self.lbl_quantum = tk.Label(root, text="Quantum (en unidades de tiempo):", bg="#010132", fg="white")
        self.lbl_quantum.pack(pady=5)
        self.txt_quantum = tk.Entry(root)
        self.txt_quantum.pack(pady=5)

        self.btn_run = tk.Button(root, text="Ejecutar Algoritmo Round Robin", command=self.run_round_robin, bg="#FF00FF", fg="white")
        self.btn_run.pack(pady=5)
        self.btn_run.bind("<Enter>", lambda e: self.on_enter(e, self.btn_run))
        self.btn_run.bind("<Leave>", lambda e: self.on_leave(e, self.btn_run))

        # Botón para mostrar el diagrama de Gantt
        self.btn_gantt = tk.Button(root, text="Mostrar Diagrama de Gantt", command=self.draw_gantt_chart, bg="#FF00FF", fg="white")
        self.btn_gantt.pack(pady=5)
        self.btn_gantt.bind("<Enter>", lambda e: self.on_enter(e, self.btn_gantt))
        self.btn_gantt.bind("<Leave>", lambda e: self.on_leave(e, self.btn_gantt))

        # Espacio para el gráfico
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(fill="both", expand=True)

        # Label para mostrar resultados finales
        self.lbl_result = tk.Label(root, text="", bg="#010132", fg="white")
        self.lbl_result.pack(pady=5)
        
         # Mensaje de derechos reservados
        self.lbl_rights = tk.Label(
            root,
            text="Ing. Eduardo Pimienta Leon. Esta obra está bajo licencia CC BY-NC-SA 4.0. "
                 "Para ver una copia de esta licencia, haga clic aquí.",
            bg="#010132",
            fg="white",
            cursor="hand2"  # Cambia el cursor para indicar que es clickeable
        )
        self.lbl_rights.pack(side="bottom", pady=10)

        # Vincula el evento de clic con el método
        self.lbl_rights.bind("<Button-1>", self.open_license_link)

    def open_license_link(self, event):
        # Método que abre el enlace en el navegador
        webbrowser.open("https://creativecommons.org/licenses/by-nc-sa/4.0/")


    def on_enter(self, event, button):
        button['bg'] = "#00FFFF"

    def on_leave(self, event, button):
        button['bg'] = "#FF00FF"

    def add_process(self):
        """Añadir proceso y su tiempo de CPU a la lista."""
        tiempo_cpu = self.txt_tiempo_cpu.get()
        if tiempo_cpu.isdigit():
            proceso = f"P{len(self.process_list) + 1}"
            self.process_list.append(proceso)
            self.burst_times.append(int(tiempo_cpu))

            # Añadir proceso a la tabla
            self.tree.insert("", "end", values=(proceso, tiempo_cpu))

            # Limpiar el campo de entrada
            self.txt_tiempo_cpu.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Introduce un número válido para el tiempo de CPU.")

    def edit_process(self):
        """Editar el proceso seleccionado."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un proceso para editar.")
            return

        item = self.tree.item(selected_item)
        proceso = item['values'][0]
        current_burst_time = item['values'][1]

        new_burst_time = self.txt_tiempo_cpu.get()
        if new_burst_time.isdigit():
            index = self.process_list.index(proceso)
            self.burst_times[index] = int(new_burst_time)
            self.tree.item(selected_item, values=(proceso, new_burst_time))
            self.txt_tiempo_cpu.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Introduce un número válido para el tiempo de CPU.")

    def delete_process(self):
        """Borrar el proceso seleccionado."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un proceso para borrar.")
            return

        item = self.tree.item(selected_item)
        proceso = item['values'][0]
        index = self.process_list.index(proceso)

        # Eliminar proceso de la lista
        del self.process_list[index]
        del self.burst_times[index]
        self.tree.delete(selected_item)

    def run_round_robin(self):
        """Ejecutar el algoritmo de Round Robin."""
        quantum = self.txt_quantum.get()
        if not quantum.isdigit():
            messagebox.showerror("Error", "Introduce un número válido para el quantum.")
            return
        
        quantum = int(quantum)
        n = len(self.process_list)
        if n == 0:
            messagebox.showwarning("Advertencia", "No hay procesos para ejecutar.")
            return

        remaining_burst = self.burst_times[:]
        waiting_time = [0] * n
        turn_around_time = [0] * n
        completion_time = [0] * n
        time = 0

        # Simulación de Round Robin
        while True:
            done = True
            for i in range(n):
                if remaining_burst[i] > 0:
                    done = False  # Aún hay procesos que ejecutar
                    # Calcular el tiempo restante tras esta iteración
                    if remaining_burst[i] > quantum:
                        time += quantum
                        remaining_burst[i] -= quantum
                    else:
                        time += remaining_burst[i]
                        remaining_burst[i] = 0
                        completion_time[i] = time  # Registrar el tiempo de finalización

            if done:
                break

        # Calcular tiempos de espera y retorno
        for i in range(n):
            turn_around_time[i] = completion_time[i]
            waiting_time[i] = turn_around_time[i] - self.burst_times[i]

        avg_waiting_time = sum(waiting_time) / n
        avg_turnaround_time = sum(turn_around_time) / n

        # Mostrar los resultados
        self.lbl_avg_waiting.config(text=f"Tiempo promedio de espera: {avg_waiting_time:.2f}")
        self.lbl_avg_turnaround.config(text=f"Tiempo promedio de retorno: {avg_turnaround_time:.2f}")

        # Dibujar el gráfico
        self.draw_graph(waiting_time, completion_time)

    def draw_graph(self, waiting_time, completion_time):
        """Dibujar gráfico de barras para el tiempo de espera y tiempo de finalización."""
        # Borrar gráfico anterior si existe
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots()

        procesos = self.process_list
        index = range(len(procesos))
        bar_width = 0.35

        # Crear barras para tiempos de espera y de finalización
        bars1 = ax.bar(index, waiting_time, bar_width, label="Tiempo de Espera", color='orange')
        bars2 = ax.bar([i + bar_width for i in index], completion_time, bar_width, label="Tiempo de Finalización", color='blue')

        # Añadir etiquetas a las barras
        for i, bar in enumerate(bars1):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{waiting_time[i]}', ha='center', va='bottom')

        for i, bar in enumerate(bars2):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{completion_time[i]}', ha='center', va='bottom')

        # Mostrar el gráfico en el widget tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_gantt_chart(self):
        """Dibujar el diagrama de Gantt para los procesos."""
        quantum = self.txt_quantum.get()
        if not quantum.isdigit():
            messagebox.showerror("Error", "Introduce un número válido para el quantum.")
            return

        quantum = int(quantum)
        n = len(self.process_list)
        if n == 0:
            messagebox.showwarning("Advertencia", "No hay procesos para mostrar el diagrama de Gantt.")
            return

        remaining_burst = self.burst_times[:]
        time = 0
        gantt_chart_data = []

        while True:
            done = True
            for i in range(n):
                if remaining_burst[i] > 0:
                    done = False  # Aún hay procesos que ejecutar
                    if remaining_burst[i] > quantum:
                        gantt_chart_data.append((f'P{i+1}', time, time + quantum))
                        time += quantum
                        remaining_burst[i] -= quantum
                    else:
                        gantt_chart_data.append((f'P{i+1}', time, time + remaining_burst[i]))
                        time += remaining_burst[i]
                        remaining_burst[i] = 0

            if done:
                break

        self.plot_gantt_chart(gantt_chart_data)

    def plot_gantt_chart(self, gantt_chart_data):
        """Dibujar el diagrama de Gantt con los datos proporcionados."""
        fig, ax = plt.subplots()

        for process, start, end in gantt_chart_data:
            ax.barh(process, end - start, left=start, color='lightblue')

        ax.set_xlabel('Tiempo')
        ax.set_title('Diagrama de Gantt')
        plt.xticks(range(0, sum(self.burst_times) + 1, 1))
        plt.grid(axis='x')

        # Mostrar el gráfico en la interfaz
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = RoundRobinApp(root)
    root.mainloop()

