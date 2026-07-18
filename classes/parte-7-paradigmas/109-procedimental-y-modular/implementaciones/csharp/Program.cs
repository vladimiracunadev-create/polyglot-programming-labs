using System;
using System.Linq;

long Promedio(int[] a) => a.Sum(x => (long) x) / a.Length;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
Console.WriteLine($"promedio={Promedio(nums)}");
