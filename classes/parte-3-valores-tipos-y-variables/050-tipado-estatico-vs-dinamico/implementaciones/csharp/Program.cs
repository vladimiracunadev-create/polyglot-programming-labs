using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0], inv);
double b = double.Parse(p[1], inv);
Console.WriteLine($"suma={(a + b).ToString("F2", inv)}");
