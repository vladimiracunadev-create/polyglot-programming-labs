using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int[] nums = p.Select(int.Parse).ToArray();
int[] copia = (int[]) nums.Clone();
copia[copia.Length - 1] = 99;
Console.WriteLine($"original={string.Join("-", nums)} copia={string.Join("-", copia)}");
