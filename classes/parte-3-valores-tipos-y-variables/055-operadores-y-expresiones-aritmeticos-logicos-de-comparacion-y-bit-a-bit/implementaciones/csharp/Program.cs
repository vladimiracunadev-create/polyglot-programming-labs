using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Console.WriteLine($"suma={a + b} resta={a - b} mult={a * b} div={a / b} mod={a % b}");
