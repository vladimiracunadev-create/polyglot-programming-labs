using System;

long Doble(long x) => x * 2; // simula P/Invoke hacia C

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Doble(n)}");
