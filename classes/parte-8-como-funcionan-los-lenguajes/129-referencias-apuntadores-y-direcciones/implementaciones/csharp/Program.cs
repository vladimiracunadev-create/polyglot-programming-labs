using System;
using System.Linq;

int[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
int indice = t[0];
Console.WriteLine($"valor={t[indice + 1]}");
