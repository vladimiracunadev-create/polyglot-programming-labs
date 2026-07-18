using System;

string tipo = Console.In.ReadToEnd().Trim();
string r = tipo switch {
    "sistemas" => "Rust",
    "web" => "TypeScript",
    "datos" => "SQL",
    _ => "Python",
};
Console.WriteLine($"lenguaje={r}");
