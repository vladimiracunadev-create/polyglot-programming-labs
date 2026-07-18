using System;

void Doblar(ref int x) {
    x *= 2;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
int antes = n;
int v = n;
Doblar(ref v);
Console.WriteLine($"antes={antes} despues={v}");
