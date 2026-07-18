using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[1]), b = long.Parse(t[2]);
long r = t[0] switch { "suma" => a + b, "resta" => a - b, _ => a * b };
Console.WriteLine($"resultado={r}");
