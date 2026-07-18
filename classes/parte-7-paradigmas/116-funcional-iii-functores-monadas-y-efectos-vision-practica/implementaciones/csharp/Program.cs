using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int? opcion = n > 0 ? n : (int?) null;
int? r = opcion.HasValue ? opcion.Value * 2 : (int?) null;
Console.WriteLine(r.HasValue ? $"resultado={r.Value}" : "resultado=nada");
