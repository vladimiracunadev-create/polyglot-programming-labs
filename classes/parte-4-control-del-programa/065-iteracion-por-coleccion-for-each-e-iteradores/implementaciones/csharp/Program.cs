using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
long suma = 0;
foreach (string s in p) {
    suma += int.Parse(s);
}
Console.WriteLine($"suma={suma}");
