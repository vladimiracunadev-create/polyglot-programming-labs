using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var a = int.Parse(p[0]);
var b = int.Parse(p[1]);
Console.WriteLine($"producto={a * b}");
