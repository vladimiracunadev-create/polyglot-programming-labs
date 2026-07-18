using System;

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long area = t[0] switch {
    "cuadrado" => long.Parse(t[1]) * long.Parse(t[1]),
    _ => long.Parse(t[1]) * long.Parse(t[2]),
};
Console.WriteLine($"area={area}");
