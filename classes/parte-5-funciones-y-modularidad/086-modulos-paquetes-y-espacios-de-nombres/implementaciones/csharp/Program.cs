using System;

// En C# las sentencias top-level deben preceder a las declaraciones de tipo.
int n = int.Parse(Console.In.ReadToEnd().Trim());
Console.WriteLine($"resultado={Matematicas.Doble(n)}");

static class Matematicas {
    public static int Doble(int n) => 2 * n;
}
