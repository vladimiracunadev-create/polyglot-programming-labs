using System;

int Doblar(int x) {
    x = x * 2;
    return x;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int local = Doblar(n);
Console.WriteLine($"original={n} local={local}");
