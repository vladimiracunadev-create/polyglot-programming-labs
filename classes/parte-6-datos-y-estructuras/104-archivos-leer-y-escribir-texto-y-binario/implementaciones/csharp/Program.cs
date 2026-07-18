using System;

string linea = Console.In.ReadToEnd().TrimEnd('\r', '\n');
int palabras = linea.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries).Length;
Console.WriteLine($"palabras={palabras} caracteres={linea.Length}");
