using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var c = new Contador();
for (int i = 0; i < n; i++) c.Incrementar();
Console.WriteLine($"cuenta={c.Cuenta}");

class Contador {
    public int Cuenta { get; private set; }
    public void Incrementar() => Cuenta++;
}
