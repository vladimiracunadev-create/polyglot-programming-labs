using System;
using System.Globalization;

var inv = CultureInfo.InvariantCulture;
int n = int.Parse(Console.In.ReadToEnd().Trim(), inv);
string par = (n % 2 == 0) ? "true" : "false";
Console.WriteLine($"entero={n} real={((double)n).ToString("F1", inv)} par={par}");
