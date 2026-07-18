using System;

int edad = int.Parse(Console.In.ReadToEnd().Trim());
if (edad < 0)
    Console.WriteLine("invalido");
else if (edad < 18)
    Console.WriteLine("menor");
else
    Console.WriteLine("adulto");
