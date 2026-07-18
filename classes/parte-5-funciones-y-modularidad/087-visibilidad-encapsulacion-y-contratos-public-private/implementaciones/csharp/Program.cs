using System;

// Las sentencias top-level van antes de la declaración del tipo.
long n = long.Parse(Console.In.ReadToEnd().Trim());
var c = new Cuenta();
c.Depositar(n);
c.Depositar(n);
Console.WriteLine($"saldo={c.Saldo()}");

class Cuenta {
    private long saldo = 0;
    public void Depositar(long monto) => saldo += monto;
    public long Saldo() => saldo;
}
