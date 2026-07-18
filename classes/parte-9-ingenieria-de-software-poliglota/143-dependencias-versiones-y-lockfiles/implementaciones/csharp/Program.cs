using System;

string[] v = Console.In.ReadToEnd().Trim().Split('.');
Console.WriteLine($"mayor={int.Parse(v[0])} menor={int.Parse(v[1])} parche={int.Parse(v[2])}");
