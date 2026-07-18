using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
(int a, int b) t = (int.Parse(p[0]), int.Parse(p[1]));
t = (t.b, t.a);
Console.WriteLine($"tupla=({t.a}, {t.b})");
