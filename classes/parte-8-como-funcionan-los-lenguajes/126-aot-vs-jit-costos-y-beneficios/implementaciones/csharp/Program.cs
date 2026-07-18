using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long r = 1;
for (int i = 0; i < n; i++) r *= 2;
Console.WriteLine($"resultado={r}");
