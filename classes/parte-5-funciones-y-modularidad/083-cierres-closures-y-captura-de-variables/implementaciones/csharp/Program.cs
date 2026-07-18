using System;

Func<int, int> HacerSumador(int baseN) => x => baseN + x;

int b = int.Parse(Console.In.ReadToEnd().Trim());
var sumar = HacerSumador(b);
Console.WriteLine($"r1={sumar(1)} r2={sumar(2)}");
