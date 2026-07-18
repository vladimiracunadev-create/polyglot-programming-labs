using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);

// C# sí ofrece asignación por tuplas.
(a, b) = (b, a);

Console.WriteLine($"a={a} b={b}");
