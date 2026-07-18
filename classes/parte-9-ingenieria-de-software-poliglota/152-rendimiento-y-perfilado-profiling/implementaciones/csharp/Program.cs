using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long ops = 0, suma = 0;
for (int i = 1; i <= n; i++) {
    suma += i;
    ops += 1;
}
Console.WriteLine($"operaciones={ops} resultado={suma}");
