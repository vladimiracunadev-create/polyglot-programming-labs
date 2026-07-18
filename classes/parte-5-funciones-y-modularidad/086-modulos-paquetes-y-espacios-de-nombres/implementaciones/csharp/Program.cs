using System;

static class Matematicas {
    public static int Doble(int n) => 2 * n;
}

int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Matematicas.Doble(n)}");
