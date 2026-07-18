using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
string Tf(bool x) => x ? "true" : "false";
bool pos = n > 0;
bool par = n % 2 == 0;
Console.WriteLine($"positivo={Tf(pos)} par={Tf(par)} ambos={Tf(pos && par)}");
