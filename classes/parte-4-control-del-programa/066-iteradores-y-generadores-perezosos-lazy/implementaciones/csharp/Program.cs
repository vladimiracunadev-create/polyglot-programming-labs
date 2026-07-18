using System;
using System.Linq;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var pares = Enumerable.Range(1, n).Select(i => 2 * i);
Console.WriteLine($"pares={string.Join("-", pares)}");
