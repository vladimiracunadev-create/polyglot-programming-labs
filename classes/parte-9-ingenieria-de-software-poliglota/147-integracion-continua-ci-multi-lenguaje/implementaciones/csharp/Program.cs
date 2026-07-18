using System;
using System.Linq;

bool verde = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .All(x => int.Parse(x) == 1);
Console.WriteLine($"ci={(verde ? "verde" : "rojo")}");
