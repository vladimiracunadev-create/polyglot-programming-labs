using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long suma = 0;
for (int i = 1; i <= n; i++) suma += i;
Console.WriteLine($"suma={suma}");
