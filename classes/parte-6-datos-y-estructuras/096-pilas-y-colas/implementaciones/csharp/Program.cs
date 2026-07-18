using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string pila = string.Join("-", p.Reverse());
string cola = string.Join("-", p);
Console.WriteLine($"pila={pila} cola={cola}");
