using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] arr = p.Take(3).Select(int.Parse).ToArray();
Console.WriteLine($"suma={arr.Sum()} max={arr.Max()}");
