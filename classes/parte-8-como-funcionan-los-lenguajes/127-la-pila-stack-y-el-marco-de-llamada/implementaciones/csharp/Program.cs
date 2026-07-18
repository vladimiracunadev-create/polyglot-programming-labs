using System;

long Sumar(int n) => n == 0 ? 0 : n + Sumar(n - 1);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"suma={Sumar(n)} profundidad={n}");
