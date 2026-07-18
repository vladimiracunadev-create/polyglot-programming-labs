using System;
using System.Collections.Generic;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var freq = new Dictionary<int, int>();
foreach (string s in p) {
    int x = int.Parse(s);
    freq[x] = freq.GetValueOrDefault(x, 0) + 1;
}
Console.WriteLine($"cuenta={freq[int.Parse(p[0])]}");
