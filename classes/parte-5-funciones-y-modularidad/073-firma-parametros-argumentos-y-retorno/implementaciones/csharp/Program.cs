using System;

int Suma(int a, int b) => a + b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(int.Parse(p[0]), int.Parse(p[1]))}");
