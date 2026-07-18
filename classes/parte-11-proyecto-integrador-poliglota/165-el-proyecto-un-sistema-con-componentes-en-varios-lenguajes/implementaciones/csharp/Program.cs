using System;

string[] c = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
Console.WriteLine($"componentes={c.Length} nombres={string.Join("-", c)}");
