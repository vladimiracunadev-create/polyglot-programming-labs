using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var p = new Persona(t[0], int.Parse(t[1]));
Console.WriteLine($"Persona(nombre={p.Nombre}, edad={p.Edad})");

record Persona(string Nombre, int Edad);
