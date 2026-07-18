using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var doblados = p.Select(int.Parse).Select(x => x * 2).ToList();
int total = doblados.Sum();
Console.WriteLine($"doblados={string.Join("-", doblados)} total={total}");
