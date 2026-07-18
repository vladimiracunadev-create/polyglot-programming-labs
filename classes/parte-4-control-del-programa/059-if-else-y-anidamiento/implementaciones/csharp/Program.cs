using System;

int score = int.Parse(Console.In.ReadToEnd().Trim());
string nota;
if (score >= 90) nota = "A";
else if (score >= 80) nota = "B";
else if (score >= 70) nota = "C";
else nota = "F";
Console.WriteLine($"nota={nota}");
