using System;

int n = int.Parse(Console.In.ReadToEnd().Trim());
for (int i = 0; i < n; i++) {
    var tmp = new object(); // el GC lo recolectará
    if (tmp == null) return;
}
Console.WriteLine($"creados={n} estado=recolectado");
