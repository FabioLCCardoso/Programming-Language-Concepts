#include <iostream>
#include <vector>
#include <algorithm>
#include <array>
#include <cmath>

#ifdef _WIN32
    #define EXPORT extern "C" __declspec(dllexport)
#else
    #define EXPORT extern "C"
#endif

/*
 Windows : g++ -O2 -shared -static -o main.dll main.cpp
 Linux : g++ -O2 -shared -fPIC -o main.so main.cpp
*/
//calcula o número de iterações do conjunto de Mandelbrot para um ponto (real, imag)
static int mandelbrot(double real, double imag, int max_iter) {
  double zr = 0;
  double zi = 0;
  int iter;

  for (iter = 0; iter < max_iter; iter++)
  {
      double new_zr = zr*zr - zi*zi + real;
      double new_zi = 2*zr*zi + imag;

      zr = new_zr;
      zi = new_zi;

      if (zr*zr + zi*zi > 4)
          return iter;
  }

  return max_iter;
}

extern "C" void calculate_mandelbrot(int *out, int width, int height, double minReal, double maxReal, double minImag, double maxImag, int max_iter) {
 double realStep = (maxReal - minReal) / (double)width;
 double imagStep = (maxImag - minImag) / (double)height;

 for(int i = 0; i < height; i++) {
   double imag = minImag + i * imagStep;

   for(int j = 0; j < width; j++) {
     double real = minReal + j * realStep;
      // armazena resultado no buffer
     out[i * width + j] = mandelbrot(real, imag, max_iter);
   }
 }

}

/*
int main(int argc, char** argv){
  const int X = 800;
  const int Y = 600;
  const double minReal = -2.0;
  const double maxReal = 1.0;
  const double minImag = -1.0;
  const double maxImag = 1.0;

  std::array<std::array<double, X>,Y> arr{};

  const int max_iter = 1000;

  for (int y = 0; y < Y; ++y) {
    for (int x = 0; x < X; ++x) {
      double real = minReal + (double)x * (maxReal - minReal)/(double)X;
      double imag = minImag + (double)y * (maxImag - minImag)/(double)Y;

      int iter = mandelbrot(real, imag, max_iter);
      arr[y][x] = iter;
    }
    std::cout << "\n";
  }
}
*/