using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int[] arr = new int[n];
long suma = 0;
for (int i = 0; i < n; i++) {
    arr[i] = i + 1;
    suma += arr[i];
}
Console.WriteLine($"reservado={n} suma={suma}");
