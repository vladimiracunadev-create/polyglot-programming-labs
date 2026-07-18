using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
Func<int, int> doblar = x => x * 2;
Func<int, int> incrementar = x => x + 1;
Func<int, int> compuesta = x => incrementar(doblar(x));
Console.WriteLine($"resultado={compuesta(n)}");
