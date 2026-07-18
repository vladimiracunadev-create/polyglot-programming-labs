using System;
using System.Threading.Tasks;

async Task<int> Doble(int x) => await Task.FromResult(x * 2);

int n = int.Parse(Console.In.ReadToEnd().Trim());
int resultado = await Doble(n);
Console.WriteLine($"resultado={resultado}");
