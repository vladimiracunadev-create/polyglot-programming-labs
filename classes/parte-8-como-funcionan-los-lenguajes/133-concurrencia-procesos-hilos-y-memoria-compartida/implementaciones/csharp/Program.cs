using System;

string[] nums = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);
int cuenta = 0;
foreach (var s in nums) cuenta += 1;
Console.WriteLine($"cuenta={cuenta}");
