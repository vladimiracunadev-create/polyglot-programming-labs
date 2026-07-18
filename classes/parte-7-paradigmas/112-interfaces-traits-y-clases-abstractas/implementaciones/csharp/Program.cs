using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
IForma f = t[0] == "cuadrado"
    ? new Cuadrado(long.Parse(t[1]))
    : new Rectangulo(long.Parse(t[1]), long.Parse(t[2]));
Console.WriteLine($"area={f.Area()}");

interface IForma { long Area(); }
class Cuadrado : IForma { long l; public Cuadrado(long l) { this.l = l; } public long Area() => l * l; }
class Rectangulo : IForma { long a, b; public Rectangulo(long a, long b) { this.a = a; this.b = b; } public long Area() => a * b; }
