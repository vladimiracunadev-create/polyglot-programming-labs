using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int x = n;
{
    int xInterno = x + 10;
    Console.WriteLine($"interno={xInterno} externo={x}");
}
