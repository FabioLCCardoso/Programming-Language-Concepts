# Fractal de Mandelbrot — C++ + Python

Trabalho da disciplina de **Conceitos de Linguagens de Programação**.

Esse projeto implementa a visualização do fractal de Mandelbrot usando duas linguagens de programação:

- **C++** — cálculo numérico do conjunto (compilado como biblioteca compartilhada).
- **Python** — interface gráfica (Tkinter) e caso de estudo também(geração de imagens PNG).

A comunicação entre as linguagens é feita via `ctypes`: o Python carrega a `.so`/`.dll` compilada em C++ e invoca diretamente a função `calculate_mandelbrot`.

---

## Arquivos do repositório

| Arquivo              | Descrição                                                        |
|----------------------|------------------------------------------------------------------|
| `main.cpp`           | Biblioteca C++ com o algoritmo de Mandelbrot                     |
| `mandelbrotUI.py`    | Interface gráfica em Python (Tkinter + ctypes)                   |
| `mandelbrot_case.py` | Caso de estudo: gera imagens PNG sem abrir a interface           |
| `Makefile`           | Compilação da biblioteca e execução dos programas                |
| `documentacao.pdf`   | Documentação da implementação (métodos, linguagens, interface)   |
| `README.md`          | Este arquivo                                                     |

---

## Dependências

### C++

- `g++` (GCC) com suporte a C++11 ou superior.

### Python 3

Existem alguns pacotes necessários (instalar via pip):

```bash
pip install Pillow numpy
```

O Tkinter já vem incluso na instalação padrão do Python
Mas no Ubuntu/Debian, caso necessário:

```bash
sudo apt install python3-tk
```

---

## Como compilar

```bash
make
```

Isso gera a biblioteca compartilhada `main.so` (Linux) ou `main.dll` (Windows).

Manualmente:

```bash
# Linux
g++ -O2 -shared -fPIC -o main.so main.cpp

# Windows
g++ -O2 -shared -static -o main.dll main.cpp
```

---

## Como executar

### Interface gráfica

```bash
make run
# ou
python3 mandelbrotUI.py
```

### Caso de estudo (sem interface gráfica)

```bash
make case
# ou
python3 mandelbrot_case.py
```

O caso de estudo gera arquivos `.png` na pasta atual com algumas diferentes regiões e configurações de iteração do fractal.

### Limpeza

```bash
make clean
```

remove a biblioteca compilada e as imagens geradas pelo caso de estudo.

O C++ exporta a função com a macro `EXPORT`, que garante compatibilidade entre sistemas:

```cpp
#ifdef _WIN32
    #define EXPORT extern "C" __declspec(dllexport)
#else
    #define EXPORT extern "C"
#endif
```

---

## Limpeza

```bash
make clean
```
