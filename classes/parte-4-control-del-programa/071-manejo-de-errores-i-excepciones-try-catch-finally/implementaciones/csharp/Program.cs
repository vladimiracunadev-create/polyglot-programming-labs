using System;

string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int a = int.Parse(p[0]);
int b = int.Parse(p[1]);
try {
    int r = a / b;
    Console.WriteLine($"resultado={r}");
} catch (DivideByZeroException) {
    Console.WriteLine("error=division por cero");
}
