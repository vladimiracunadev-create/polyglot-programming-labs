using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var r = Enumerable.Range(a, b - a + 1).ToList();
Console.WriteLine($"rango={string.Join("-", r)} suma={r.Sum()}");
