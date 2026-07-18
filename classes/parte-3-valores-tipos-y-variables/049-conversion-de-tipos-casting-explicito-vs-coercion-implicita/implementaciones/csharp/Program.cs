using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
double f = double.Parse(Console.In.ReadToEnd().Trim(), inv);
Console.WriteLine($"entero={(long)f} real={f.ToString("F2", inv)}");
