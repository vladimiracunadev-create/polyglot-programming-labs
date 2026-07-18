using System;

class Cuenta {
    private long saldo = 0;
    public void Depositar(long monto) => saldo += monto;
    public long Saldo() => saldo;
}

long n = long.Parse(Console.In.ReadToEnd().Trim());
var c = new Cuenta();
c.Depositar(n);
c.Depositar(n);
Console.WriteLine($"saldo={c.Saldo()}");
