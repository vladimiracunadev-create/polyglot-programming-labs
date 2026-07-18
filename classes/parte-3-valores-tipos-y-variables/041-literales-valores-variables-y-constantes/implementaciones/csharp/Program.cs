using System;
using System.Globalization;

// C# sobre el CLR: tipado estático con cultura invariante para el formato.
string[] p = Console.In.ReadToEnd()
    .Split(new[] { ' ', '\t', '\n', '\r' }, StringSplitOptions.RemoveEmptyEntries);

double precioUnitario = double.Parse(p[0], CultureInfo.InvariantCulture);
int cantidad = int.Parse(p[1], CultureInfo.InvariantCulture);
double descuento = double.Parse(p[2], CultureInfo.InvariantCulture);

double subtotal = precioUnitario * cantidad;
double total = subtotal * (1 - descuento);

Console.WriteLine("Total: " + total.ToString("F2", CultureInfo.InvariantCulture));
