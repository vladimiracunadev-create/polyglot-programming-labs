using System;
using System.Text;

int n = int.Parse(Console.In.ReadToEnd().Trim());
long acc = 0;
var sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    acc += i;
    if (i > 1) sb.Append("-");
    sb.Append(acc);
}
Console.WriteLine($"traza={sb}");
