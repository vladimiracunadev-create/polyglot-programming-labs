using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pares = p.Select(int.Parse).Where(x => x % 2 == 0);
Console.WriteLine($"pares={string.Join("-", pares)}");
