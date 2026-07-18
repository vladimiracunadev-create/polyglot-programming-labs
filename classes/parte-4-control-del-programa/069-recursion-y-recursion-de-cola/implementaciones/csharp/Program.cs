using System;

long Fib(int n) => n < 2 ? n : Fib(n - 1) + Fib(n - 2);

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"fib={Fib(n)}");
