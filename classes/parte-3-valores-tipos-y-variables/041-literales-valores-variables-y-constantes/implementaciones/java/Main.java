import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");

        // Tipado estático nominal: cada valor declara su tipo.
        final double precioUnitario = Double.parseDouble(p[0]);
        final int cantidad = Integer.parseInt(p[1]);
        final double descuento = Double.parseDouble(p[2]);

        double subtotal = precioUnitario * cantidad;
        double total = subtotal * (1 - descuento);

        System.out.printf(Locale.US, "Total: %.2f%n", total);
    }
}
