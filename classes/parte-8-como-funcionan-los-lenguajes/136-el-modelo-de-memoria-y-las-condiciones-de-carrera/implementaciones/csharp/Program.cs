using System;
using System.Threading;

int n = int.Parse(Console.In.ReadToEnd().Trim());
int cuenta = 0;
for (int i = 0; i < n; i++) Interlocked.Increment(ref cuenta);
Console.WriteLine($"cuenta={cuenta}");
