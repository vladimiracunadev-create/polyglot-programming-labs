using System;

string tipo = Console.In.ReadToEnd().Trim();
IAnimal a = tipo switch {
    "perro" => new Perro(),
    "gato" => new Gato(),
    _ => new Vaca(),
};
Console.WriteLine($"sonido={a.Sonido()}");

interface IAnimal { string Sonido(); }
class Perro : IAnimal { public string Sonido() => "guau"; }
class Gato : IAnimal { public string Sonido() => "miau"; }
class Vaca : IAnimal { public string Sonido() => "muu"; }
