using System;
using System.Collections.Generic;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var almacen = new Dictionary<string, string>();
almacen[p[0]] = p[1];
Console.WriteLine($"guardado={p[0]}={almacen[p[0]]}");
