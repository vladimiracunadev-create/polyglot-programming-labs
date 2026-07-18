using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
string nombre = t[0];
int edad = int.Parse(t[1]);
Console.WriteLine($"{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
