using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(t[0]), b = long.Parse(t[2]);
long r = t[1] switch { "+" => a + b, "-" => a - b, _ => a * b };
Console.WriteLine($"resultado={r}");
