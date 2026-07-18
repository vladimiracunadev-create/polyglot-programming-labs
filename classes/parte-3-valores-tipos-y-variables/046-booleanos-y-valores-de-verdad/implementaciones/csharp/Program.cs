using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
bool a = int.Parse(p[0]) != 0;
bool b = int.Parse(p[1]) != 0;
string Tf(bool x) => x ? "true" : "false";
Console.WriteLine($"and={Tf(a && b)} or={Tf(a || b)} not_a={Tf(!a)}");
