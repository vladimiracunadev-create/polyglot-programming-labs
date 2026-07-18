using System;

long Doble(long x) => x * 2;
string Wrapper(long x) => $"wrap({Doble(x)})";

long n = long.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"envuelto={Wrapper(n)}");
