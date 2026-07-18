using System;

(int? ok, string err) Dividir(int a, int b) =>
    b == 0 ? (null, "division") : (a / b, null);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
var (ok, err) = Dividir(a, b);
Console.WriteLine(err != null ? $"err={err}" : $"ok={ok}");
