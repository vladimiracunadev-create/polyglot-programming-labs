using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool valido = w.Length > 0 && w.All(c => c >= 'a' && c <= 'z');
Console.WriteLine($"valido={(valido ? "true" : "false")}");
