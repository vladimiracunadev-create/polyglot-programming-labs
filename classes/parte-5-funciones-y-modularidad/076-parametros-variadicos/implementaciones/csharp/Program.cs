using System;
using System.Linq;

long Suma(params int[] nums) => nums.Sum(x => (long) x);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"suma={Suma(p.Select(int.Parse).ToArray())}");
