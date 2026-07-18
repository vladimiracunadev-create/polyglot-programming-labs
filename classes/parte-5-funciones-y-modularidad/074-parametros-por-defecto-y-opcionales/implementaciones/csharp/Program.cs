using System;

long Potencia(long baseN, int exp = 2) {
    long r = 1;
    for (int i = 0; i < exp; i++) r *= baseN;
    return r;
}

string[] t = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long b = long.Parse(t[0]);
long res = t.Length > 1 ? Potencia(b, int.Parse(t[1])) : Potencia(b);
Console.WriteLine($"resultado={res}");
