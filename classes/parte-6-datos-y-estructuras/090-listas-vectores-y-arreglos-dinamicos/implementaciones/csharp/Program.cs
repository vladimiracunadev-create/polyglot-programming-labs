using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var nums = p.Select(int.Parse).Reverse();
Console.WriteLine($"invertido={string.Join("-", nums)}");
