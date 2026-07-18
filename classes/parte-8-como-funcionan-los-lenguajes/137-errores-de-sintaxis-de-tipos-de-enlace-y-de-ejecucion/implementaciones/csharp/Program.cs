using System;

int codigo = int.Parse(Console.In.ReadToEnd().Trim());
string e = codigo switch {
    1 => "sintaxis",
    2 => "tipos",
    3 => "enlace",
    4 => "ejecucion",
    _ => "desconocido",
};
Console.WriteLine($"error={e}");
