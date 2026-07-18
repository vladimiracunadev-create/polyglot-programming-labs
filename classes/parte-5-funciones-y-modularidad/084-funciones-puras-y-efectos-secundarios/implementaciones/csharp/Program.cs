using System;

long Cuadrado(long n) => n * n;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"puro={Cuadrado(n)}");
