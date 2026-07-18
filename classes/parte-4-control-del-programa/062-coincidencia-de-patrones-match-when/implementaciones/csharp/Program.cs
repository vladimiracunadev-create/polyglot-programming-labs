using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string signo = n switch {
    > 0 => "positivo",
    < 0 => "negativo",
    _ => "cero",
};
Console.WriteLine($"signo={signo}");
