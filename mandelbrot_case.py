"""

caso de estudo do fractal de Mandelbrot

gera imagens em PNG de diferentes regiões e configurações do conjunto de
Mandelbrot, sem abrir a interface gráfica. Utiliza a mesma biblioteca
compilada em C++ (main.so / main.dll) por meio de ctypes.

uso:
    python3 mandelbrot_case.py
    # ou
    make case
"""

import ctypes
import os
import sys

import numpy as np
from PIL import Image


# Carregamento da biblioteca C++


if sys.platform == "win32":
    LIB_NAME = "main.dll"
else:
    LIB_NAME = "main.so"

LIB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), LIB_NAME)

if not os.path.exists(LIB_PATH):
    print(f"Erro: biblioteca '{LIB_NAME}' não encontrada em {LIB_PATH}")
    print("Compile antes com: make")
    sys.exit(1)

lib = ctypes.CDLL(LIB_PATH)
lib.calculate_mandelbrot.restype = None
lib.calculate_mandelbrot.argtypes = [
    ctypes.POINTER(ctypes.c_int),   # out  — buffer de saída
    ctypes.c_int,                   # width
    ctypes.c_int,                   # height
    ctypes.c_double,                # minReal
    ctypes.c_double,                # maxReal
    ctypes.c_double,                # minImag
    ctypes.c_double,                # maxImag
    ctypes.c_int,                   # max_iter
]


# Funções auxiliares

def calcular(width: int, height: int, bounds: list, max_iter: int) -> np.ndarray:
    """chama a função C++ e retorna a matriz de iterações."""
    buf = (ctypes.c_int * (width * height))()
    lib.calculate_mandelbrot(
        buf, width, height,
        bounds[0], bounds[1], bounds[2], bounds[3],
        max_iter,
    )
    return np.frombuffer(buf, dtype=np.int32).reshape(height, width)


def colorir(iters: np.ndarray, max_iter: int) -> np.ndarray:
    """converte a matriz de iterações em uma imagem RGB."""
    t = np.log1p(iters.astype(float)) / np.log1p(max_iter)
    t = np.clip(t, 0.0, 1.0)

    r = (t * 100).astype(np.uint8)
    g = (t * 180).astype(np.uint8)
    b = (t * 255).astype(np.uint8)

    inside = iters >= max_iter
    r[inside] = g[inside] = b[inside] = 0

    return np.stack([r, g, b], axis=-1)


def salvar(nome: str, iters: np.ndarray, max_iter: int):
    """salva a imagem PNG a partir da matriz de iterações."""
    rgb = colorir(iters, max_iter)
    img = Image.fromarray(rgb, mode="RGB")
    img.save(nome)
    print(f"  -> {nome}  ({img.width}x{img.height}, max_iter={max_iter})")

# Aqui estão os casos de estudo

CASES = [
    {
        "nome": "mandelbrot_case_visao_geral.png",
        "descricao": "Visão geral do conjunto de Mandelbrot",
        "bounds": [-2.5, 1.0, -1.2, 1.2],
        "max_iter": 256,
    },
    {
        "nome": "mandelbrot_case_seahorse.png",
        "descricao": "Região Seahorse Valley (zoom)",
        "bounds": [-0.77, -0.73, 0.05, 0.09],
        "max_iter": 512,
    },
    {
        "nome": "mandelbrot_case_espiral.png",
        "descricao": "espiral próxima ao bulbo principal",
        "bounds": [-0.088, -0.064, 0.654, 0.672],
        "max_iter": 1024,
    },
]

WIDTH  = 800
HEIGHT = 600

def main():
    print("Caso de estudo — Fractal de Mandelbrot\n")
    for caso in CASES:
        print(f"[{caso['descricao']}]")
        iters = calcular(WIDTH, HEIGHT, caso["bounds"], caso["max_iter"])
        salvar(caso["nome"], iters, caso["max_iter"])
    print("\nConcluído.")

if __name__ == "__main__":
    main()
