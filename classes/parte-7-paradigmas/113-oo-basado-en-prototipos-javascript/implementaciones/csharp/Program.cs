using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var obj = new Obj(n);
Console.WriteLine($"resultado={obj.Doble()}");

class Obj {
    int valor;
    public Obj(int v) { valor = v; }
    public int Doble() => valor * 2;
}
