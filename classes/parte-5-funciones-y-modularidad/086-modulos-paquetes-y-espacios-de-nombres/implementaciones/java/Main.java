import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Clase de utilidades como espacio de nombres.
    static class Matematicas {
        static int doble(int n) {
            return 2 * n;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.println("resultado=" + Matematicas.doble(n));
    }
}
