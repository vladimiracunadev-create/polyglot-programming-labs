using System;
using System.Collections.Generic;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var pila = new Stack<long>();
pila.Push(long.Parse(t[0]));
pila.Push(long.Parse(t[1]));
long y = pila.Pop(), x = pila.Pop();
long r = t[2] switch { "+" => x + y, "-" => x - y, _ => x * y };
Console.WriteLine($"resultado={r}");
