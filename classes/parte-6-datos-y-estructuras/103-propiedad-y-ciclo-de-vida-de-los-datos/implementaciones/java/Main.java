import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Recurso implements AutoCloseable {
        final int valor;
        Recurso(int v) { this.valor = v; }
        public void close() { /* se libera aquí */ }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int valor;
        try (Recurso r = new Recurso(n)) {
            valor = r.valor;
        }
        System.out.println("valor=" + valor + " estado=liberado");
    }
}
