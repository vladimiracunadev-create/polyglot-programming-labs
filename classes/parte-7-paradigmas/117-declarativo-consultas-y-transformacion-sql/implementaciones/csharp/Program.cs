using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = p.Select(int.Parse).Where(x => x % 2 == 0).Sum(x => (long) x);
Console.WriteLine($"suma_pares={suma}");
