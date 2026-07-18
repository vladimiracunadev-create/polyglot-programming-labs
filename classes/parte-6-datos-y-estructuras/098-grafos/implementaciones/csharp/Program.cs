using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int aristas = p.Length / 2;
int nodos = p.Select(int.Parse).Distinct().Count();
Console.WriteLine($"aristas={aristas} nodos={nodos}");
