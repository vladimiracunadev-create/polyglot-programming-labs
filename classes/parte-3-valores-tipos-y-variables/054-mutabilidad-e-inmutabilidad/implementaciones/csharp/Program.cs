using System;
using System.Text;

int n = int.Parse(Console.In.ReadToEnd().Trim());
var sb = new StringBuilder();
for (int i = 1; i <= n; i++) {
    if (i > 1) sb.Append("-");
    sb.Append(i);
}
Console.WriteLine($"sec={sb}");
