using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long f = 1;
for (int i = 1; i <= n; i++) {
    f *= i;
}
Console.WriteLine($"factorial={f}");
