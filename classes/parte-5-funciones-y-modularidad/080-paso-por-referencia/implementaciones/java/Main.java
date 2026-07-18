import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java pasa la referencia del arreglo: se puede mutar su contenido.
    static void doblar(int[] caja) {
        caja[0] *= 2;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int antes = n;
        int[] caja = { n };
        doblar(caja);
        System.out.println("antes=" + antes + " despues=" + caja[0]);
    }
}
