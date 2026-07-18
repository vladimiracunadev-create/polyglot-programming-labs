using System;

int[] p = Array.ConvertAll(Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries), int.Parse);
Console.WriteLine($"e2e={(p[0] + p[1] == p[2] ? "pasa" : "falla")}");
