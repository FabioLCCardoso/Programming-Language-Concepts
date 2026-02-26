# Fractal de Mandelbrot — C++ + Python

Trabalho da disciplina de Conceitos de Linguagens de Programação.

O projeto implementa o fractal de Mandelbrot utilizando **duas linguagens de programação com vocações distintas**:

- **C++** realiza o cálculo numérico do conjunto
- **Python** oferece a interface gráfica e apresenta a imagem gerada

A comunicação entre as linguagens é feita via `ctypes`, que permite ao Python carregar e chamar funções de uma biblioteca compilada em C++.

---

## Arquivos do repositório

| Arquivo | Descrição |
|---------|-----------|
| `main.cpp` | Biblioteca C++ com o algoritmo de Mandelbrot |
| `mandelbrotUI.py` | Interface gráfica em Python (Tkinter) |
| `Makefile` | Compilação e execução do projeto |
| `documentacao.pdf` | Documentação da implementação |
| `README.md` | Readme |

---

## Dependências

### C++
- `g++` com suporte a C++17

### Python 3
```
pip install Pillow numpy
```

> Tkinter já vem incluso na instalação padrão do Python.  
> No Ubuntu/Debian, se necessário: `sudo apt install python3-tk`

---

## Como compilar

**Windows:**
```powershell
g++ -O2 -shared -static -o main.dll main.cpp
```

**Linux:**
```bash
g++ -O2 -shared -fPIC -o main.so main.cpp
```

Ou simplesmente:
```bash
make
```

---

## Como executar

### Interface gráfica

**Windows:**
```powershell
py -3.13-32 mandelbrotUI.py
```

**Linux:**
```bash
make run
# ou
python3 mandelbrotUI.py
```


## Como funciona

O Python carrega a biblioteca compilada em C++ usando `ctypes`:

```python
lib = ctypes.CDLL("main.dll")  # Windows
lib = ctypes.CDLL("main.so")   # Linux

lib.calculate_mandelbrot(buf, width, height,
                         minReal, maxReal,
                         minImag, maxImag,
                         max_iter)
```

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
