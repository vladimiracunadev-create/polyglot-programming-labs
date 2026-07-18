using System;
using System.Linq;

int[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries)
    .Select(int.Parse).ToArray();
int medio = nums.Length / 2;
long p1 = nums.Take(medio).Sum(x => (long) x);
long p2 = nums.Skip(medio).Sum(x => (long) x);
Console.WriteLine($"suma={p1 + p2}");
