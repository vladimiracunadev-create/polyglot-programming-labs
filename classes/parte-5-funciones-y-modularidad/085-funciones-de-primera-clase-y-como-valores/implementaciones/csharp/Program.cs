using System;

int Aplicar(Func<int, int, int> f, int a, int b) => f(a, b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Func<int, int, int> suma = (x, y) => x + y;
Func<int, int, int> producto = (x, y) => x * y;
Console.WriteLine($"suma={Aplicar(suma, a, b)} producto={Aplicar(producto, a, b)}");
