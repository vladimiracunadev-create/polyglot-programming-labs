using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long suma = 0;
int i = 1;
while (i <= n) {
    suma += i;
    i++;
}
Console.WriteLine($"suma={suma}");
