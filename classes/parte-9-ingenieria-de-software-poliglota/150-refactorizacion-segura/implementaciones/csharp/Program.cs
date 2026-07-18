using System;

long n = long.Parse(Console.In.ReadToEnd().Trim());
long viejo = n * 2, nuevo = n + n;
Console.WriteLine($"equivalente={(viejo == nuevo ? "true" : "false")} resultado={nuevo}");
