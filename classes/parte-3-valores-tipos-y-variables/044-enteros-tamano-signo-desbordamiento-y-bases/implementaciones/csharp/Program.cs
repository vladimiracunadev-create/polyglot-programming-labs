using System;
using System.Globalization;

int n = int.Parse(Console.In.ReadToEnd().Trim(), CultureInfo.InvariantCulture);
Console.WriteLine($"dec={n} hex={Convert.ToString(n, 16)} oct={Convert.ToString(n, 8)} bin={Convert.ToString(n, 2)}");
