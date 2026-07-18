using System;

(int, int) Divmod(int a, int b) => (a / b, a % b);

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
var (q, r) = Divmod(int.Parse(p[0]), int.Parse(p[1]));
Console.WriteLine($"cociente={q} resto={r}");
