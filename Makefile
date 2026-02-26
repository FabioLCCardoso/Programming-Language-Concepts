# =============================================================================
# Makefile — Fractal de Mandelbrot (C++ + Python)
# =============================================================================
# Entradas:
#   make          -> compila a biblioteca compartilhada (main.so / main.dll)
#   make run      -> executa a interface gráfica (mandelbrotUI.py)
#   make case     -> executa o caso de estudo (mandelbrot_case.py)
#   make clean    -> remove artefatos de compilação
# =============================================================================

CXX      := g++
CXXFLAGS := -O2 -shared -fPIC
SRC      := main.cpp
PYTHON   := python3

# Detecta o sistema operacional
ifeq ($(OS),Windows_NT)
	LIB := main.dll
	CXXFLAGS := -O2 -shared -static
else
	LIB := main.so
endif

# --- Compilação da biblioteca compartilhada --------------------------------
all: $(LIB)

$(LIB): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $<

# --- Execução da interface gráfica -----------------------------------------
run: $(LIB)
	$(PYTHON) mandelbrotUI.py

# --- Execução do caso de estudo --------------------------------------------
case: $(LIB)
	$(PYTHON) mandelbrot_case.py

# --- Limpeza ---------------------------------------------------------------
clean:
	rm -f $(LIB) mandelbrot_case_*.png

.PHONY: all run case clean
