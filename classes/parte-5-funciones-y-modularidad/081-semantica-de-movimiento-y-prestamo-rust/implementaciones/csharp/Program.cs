using System;

string s = Console.In.ReadToEnd().Trim();
int longitud = s.Length; // GC: la cadena permanece.
Console.WriteLine($"movido={s} longitud={longitud}");
