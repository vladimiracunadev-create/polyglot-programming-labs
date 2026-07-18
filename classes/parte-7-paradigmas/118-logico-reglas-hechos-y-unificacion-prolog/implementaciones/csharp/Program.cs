using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long a = long.Parse(p[0]);
long b = long.Parse(p[1]);
Console.WriteLine($"divisor={(b % a == 0 ? "true" : "false")}");
