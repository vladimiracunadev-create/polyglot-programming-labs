using System;
using System.Collections.Generic;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var lista = new List<int>();
for (int i = n; i >= 1; i--) lista.Add(i);
Console.WriteLine($"lista={string.Join("-", lista)}");
