using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int valor;
using (var r = new Recurso(n)) {
    valor = r.Valor;
}
Console.WriteLine($"valor={valor} estado=liberado");

class Recurso : IDisposable {
    public int Valor { get; }
    public Recurso(int v) { Valor = v; }
    public void Dispose() { /* se libera aquí */ }
}
