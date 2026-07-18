using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int d = 2;
for (; d <= n; d++) {
    if (n % d == 0) break;
}
Console.WriteLine($"primer_divisor={d}");
