using System;

T Mayor<T>(T a, T b) where T : IComparable<T> => a.CompareTo(b) > 0 ? a : b;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
Console.WriteLine($"max={Mayor(a, b)}");
