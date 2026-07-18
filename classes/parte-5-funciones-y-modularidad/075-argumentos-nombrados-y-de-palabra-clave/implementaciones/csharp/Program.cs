using System;

string Punto(int x, int y) => $"punto(x={x}, y={y})";

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine(Punto(x: int.Parse(p[0]), y: int.Parse(p[1])));
