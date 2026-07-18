using System;
using System.Linq;

string w = Console.In.ReadToEnd().Trim();
bool seguro = w.Length > 0 && w.All(char.IsLetterOrDigit);
Console.WriteLine($"seguro={(seguro ? "true" : "false")}");
