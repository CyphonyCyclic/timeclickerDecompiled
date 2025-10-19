import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
coords = {'x': 0, 'y': 0}

def capturar_coordenadas():
    messagebox.showinfo('Captura', 'Coloca el puntero en el punto donde quieres hacer clic.\nTienes 3 segundos...')
    ventana.withdraw()
    time.sleep(3)
    x, y = pyautogui.position()
    coords['x'], coords['y'] = (x, y)
    ventana.deiconify()
    entry_x.delete(0, tk.END)
    entry_y.delete(0, tk.END)
    entry_x.insert(0, str(x))
    entry_y.insert(0, str(y))
    messagebox.showinfo('Coordenadas capturadas', f'X={x}, Y={y}')

def programar_click():
    try:
        if not entry_x.get() or not entry_y.get():
            messagebox.showwarning('Faltan datos', 'Primero captura las coordenadas.')
            return
        x = int(entry_x.get())
        y = int(entry_y.get())
        hora = int(combo_hora.get())
        minuto = int(combo_minuto.get())
        segundo = int(combo_segundo.get())
        hora_programada = f'{hora:02}:{minuto:02}:{segundo:02}'

        def esperar_y_clickear():
            while True:
                ahora = datetime.now().time()
                if (ahora.hour, ahora.minute, ahora.second) == (hora, minuto, segundo):
                    pyautogui.click(x, y)
                    messagebox.showinfo('Hecho', f'Click realizado en ({x},{y}) a las {hora_programada}')
                    return
                time.sleep(0.5)
        threading.Thread(target=esperar_y_clickear, daemon=True).start()
        messagebox.showinfo('Programado', f'Click programado a las {hora_programada}')
    except Exception as e:
        messagebox.showerror('Error', str(e))
        
        
ventana = tk.Tk()
ventana.title('AutoClicker Programable')
ventana.geometry('300x320')
ventana.resizable(False, False)



tk.Label(ventana, text='Coordenadas del clic').pack(pady=5)
frame_coords = tk.Frame(ventana)
frame_coords.pack()


tk.Label(frame_coords, text='X:').grid(row=0, column=0)

entry_x = tk.Entry(frame_coords, width=10)
entry_x.grid(row=0, column=1, padx=5)


tk.Label(frame_coords, text='Y:').grid(row=0, column=2)

entry_y = tk.Entry(frame_coords, width=10)
entry_y.grid(row=0, column=3, padx=5)


tk.Button(ventana, text='Capturar coordenadas', command=capturar_coordenadas).pack(pady=10)


tk.Label(ventana, text='Hora del clic').pack(pady=5)

frame_hora = tk.Frame(ventana)
frame_hora.pack()


combo_hora = ttk.Combobox(frame_hora, values=[f'{i:02}' for i in range(24)], width=3)
combo_hora.set('00')
combo_hora.grid(row=0, column=0)

tk.Label(frame_hora, text=':').grid(row=0, column=1)

combo_minuto = ttk.Combobox(frame_hora, values=[f'{i:02}' for i in range(60)], width=3)
combo_minuto.set('00')
combo_minuto.grid(row=0, column=2)

tk.Label(frame_hora, text=':').grid(row=0, column=3)

combo_segundo = ttk.Combobox(frame_hora, values=[f'{i:02}' for i in range(60)], width=3)
combo_segundo.set('00')

combo_segundo.grid(row=0, column=4)

tk.Button(ventana, text='Programar Click', command=programar_click).pack(pady=20)

ventana.mainloop()