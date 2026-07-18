using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
Console.WriteLine($"invertido={new string(w.Reverse().ToArray())}");
