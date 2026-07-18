using System;
using System.Linq;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var stream = p.Select(int.Parse).Where(x => x % 2 == 0).Select(x => x * 2);
Console.WriteLine($"stream={string.Join("-", stream)}");
