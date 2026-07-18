using System;

long Doble(long x) => x * 2;

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Doble(n)}");
