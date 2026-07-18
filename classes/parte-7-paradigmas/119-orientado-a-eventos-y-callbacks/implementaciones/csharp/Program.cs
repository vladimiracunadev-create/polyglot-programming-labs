using System;
using System.Collections.Generic;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var recolectados = new List<int>();
Action<int> alEvento = i => recolectados.Add(i);
for (int i = 1; i <= n; i++) alEvento(i);
Console.WriteLine($"eventos={string.Join("-", recolectados)}");
