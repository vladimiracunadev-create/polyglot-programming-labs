using System;

var actor = new Acumulador();
foreach (string s in Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries))
    actor.Recibir(int.Parse(s));
Console.WriteLine($"total={actor.Total}");

class Acumulador {
    public long Total { get; private set; }
    public void Recibir(int m) => Total += m;
}
