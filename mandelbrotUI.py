"""
interface gráfica para o fractal de Mandelbrot.

este módulo implementa a camada de apresentação do projeto usando Tkinter.
Ele carrega a biblioteca compartilhada compilada em C++ (main.so / main.dll)
através do módulo ctypes da biblioteca padrão do Python e invoca a função
calculate_mandelbrot para obter a matriz de iterações e converte o resultado
em uma imagem RGB exibida no canvas.

Dependências:
    - Python 3 (com tkinter)
    - numpy
    - Pillow (PIL)
    - biblioteca compilada: main.so (Linux) ou main.dll (Windows)

Uso:
    python3 mandelbrotUI.py
    # ou
    make run
"""

import ctypes
import os
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
from PIL import Image, ImageTk

# Carregamento da biblioteca C++ via ctypes


if sys.platform == "win32":
    LIB_NAME = "main.dll"
else:
    LIB_NAME = "main.so"

LIB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), LIB_NAME)

def loadLib():
    """
    carrega a biblioteca compartilhada C++ e configura os tipos dos
    argumentos e do retorno da função calculate_mandelbrot.
    retorna o objeto ctypes.CDLL pronto para uso.
    encerra o programa com mensagem de erro caso a biblioteca não exista.
    """
    if not os.path.exists(LIB_PATH):
        messagebox.showerror(
            "Erro",
            f"Biblioteca não encontrada: {LIB_PATH}\n\n"
            "Compile com:\n"
            "  make\n"
            "  ou g++ -O2 -shared -fPIC -o main.so main.cpp (Linux)"
        )
        sys.exit(1)
    lib = ctypes.CDLL(LIB_PATH)

    # Protótipo: void calculate_mandelbrot(int*, int, int, double, double, double, double, int)
    lib.calculate_mandelbrot.restype  = None
    lib.calculate_mandelbrot.argtypes = [
        ctypes.POINTER(ctypes.c_int),  # out — buffer de saída
        ctypes.c_int,                  # width
        ctypes.c_int,                  # height
        ctypes.c_double,               # minReal
        ctypes.c_double,               # maxReal
        ctypes.c_double,               # minImag
        ctypes.c_double,               # maxImag
        ctypes.c_int,                  # max_iter
    ]
    return lib

def colorir(iters: np.ndarray, max_iter: int) -> np.ndarray:
    """
    converte a matriz de contagens de iteração em uma imagem RGB (H x W x 3).
    utiliza escala logarítmica para suavizar o gradiente de cores.
    pontos que pertencem ao conjunto (iter >= max_iter) são pintados de preto.
    """
    t = np.log1p(iters.astype(float)) / np.log1p(max_iter)
    t = np.clip(t, 0.0, 1.0)

    r = (t * 100).astype(np.uint8)
    g = (t * 180).astype(np.uint8)
    b = (t * 255).astype(np.uint8)

    # Pontos do conjunto: preto
    inside = iters >= max_iter
    r[inside] = g[inside] = b[inside] = 0

    return np.stack([r, g, b], axis=-1)

class App:
    """
    classe principal da interface gráfica.
    cria uma janela Tkinter com controles para configurar o número de
    iterações, renderizar o fractal e resetar a visualização.
    a renderização invoca a função C++ calculate_mandelbrot e exibe
    o resultado como imagem no canvas.
    """
    W, H = 700, 500
    Bounds_Default = [-2.5, 1.0, -1.2, 1.2]  # minReal, maxReal, minImag, maxImag

    def __init__(self, root: tk.Tk, lib):
        self.root   = root
        self.lib    = lib
        self.bounds = self.Bounds_Default.copy()

        root.title("Mandelbrot")
        root.resizable(False, False)

        # controles no topo
        topo = tk.Frame(root, pady=6, padx=8)
        topo.pack(fill=tk.X)

        tk.Label(topo, text="Iterações:").pack(side=tk.LEFT)
        self.iter_var = tk.IntVar(value=256)
        tk.Spinbox(topo, from_=64, to=2048, increment=64,
                   textvariable=self.iter_var, width=6).pack(side=tk.LEFT, padx=(4, 16))

        tk.Button(topo, text="Renderizar", command=self.renderizar).pack(side=tk.LEFT, padx=4)
        tk.Button(topo, text="Resetar",    command=self.resetar).pack(side=tk.LEFT, padx=4)

        # canvas
        self.canvas = tk.Canvas(root, width=self.W, height=self.H, cursor="crosshair")
        self.canvas.pack(padx=8, pady=(0, 4))

        # variáveis para seleção de zoom com o mouse
        self._sel_start = None   
        self._sel_rect  = None   

        # Eventos de mouse para zoom por seleção retangular
        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        self.canvas.bind("<B1-Motion>",       self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        # Barra de status
        self.status = tk.StringVar(value="")
        tk.Label(root, textvariable=self.status, anchor=tk.W,
                 fg="gray").pack(fill=tk.X, padx=8, pady=(0, 6))

        self.renderizar()

    def renderizar(self):
        """chamar a biblioteca C++ para calcular o conjunto e exibe a imagem no canvas."""
        W, H     = self.W, self.H
        max_iter = self.iter_var.get()
        mR, MR, mI, MI = self.bounds

        self.status.set("Calculando…")
        self.root.update_idletasks()

        buf = (ctypes.c_int * (W * H))()
        self.lib.calculate_mandelbrot(buf, W, H, mR, MR, mI, MI, max_iter)

        iters    = np.frombuffer(buf, dtype=np.int32).reshape(H, W)
        rgb      = colorir(iters, max_iter)
        img      = Image.fromarray(rgb, mode="RGB")
        self._photo = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self._photo)
        self.status.set(f"Re [{mR:.3f}, {MR:.3f}]  Im [{mI:.3f}, {MI:.3f}]  iter={max_iter}")

    def resetar(self):
        """restaura os limites padrão e rerenderiza."""
        self.bounds = self.Bounds_Default.copy()
        self.renderizar()

    def _on_press(self, event):
        """isso registra o ponto inicial da seleção e cria o retângulo visual."""
        self._sel_start = (event.x, event.y)
        if self._sel_rect:
            self.canvas.delete(self._sel_rect)
        self._sel_rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="white", width=1, dash=(4, 4)
        )

    def _on_drag(self, event):
        """atualiza o retângulo de seleção enquanto o mouse é arrastado."""
        if self._sel_start and self._sel_rect:
            x0, y0 = self._sel_start
            self.canvas.coords(self._sel_rect, x0, y0, event.x, event.y)

    def _on_release(self, event):
        """
        finaliza a seleção: converte as coordenadas de pixel para o plano
        complexo, atualiza os limites (bounds) e rerenderiza com zoom.
        Ignora seleções menores que 5 pixels pra evitar zoom acidental.
        """
        if not self._sel_start:
            return

        x0, y0 = self._sel_start
        x1, y1 = event.x, event.y
        self._sel_start = None

        if self._sel_rect:
            self.canvas.delete(self._sel_rect)
            self._sel_rect = None

        # ignora seleções muito pequenas
        if abs(x1 - x0) < 5 or abs(y1 - y0) < 5:
            return

        # vai garantir que (x0, y0) seja o canto superior esquerdo
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0

        # converte pixels para coordenadas no plano complexo
        re0, im0 = self._px(x0, y0)
        re1, im1 = self._px(x1, y1)

        self.bounds = [re0, re1, im0, im1]
        self.renderizar()

    def _px(self, x, y):
        """converte as coordenadas de pixel (x, y) para o plano complexo."""
        mR, MR, mI, MI = self.bounds
        return (mR + x / self.W * (MR - mR),
                mI + y / self.H * (MI - mI))
    
if __name__ == "__main__":
    lib  = loadLib()
    root = tk.Tk()
    App(root, lib)
    root.mainloop()