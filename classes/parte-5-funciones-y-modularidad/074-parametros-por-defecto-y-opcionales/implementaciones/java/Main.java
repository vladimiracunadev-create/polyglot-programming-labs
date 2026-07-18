import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene defectos: se simula con sobrecarga.
    static long potencia(long base) {
        return potencia(base, 2);
    }

    static long potencia(long base, int exp) {
        long r = 1;
        for (int i = 0; i < exp; i++) r *= base;
        return r;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long base = Long.parseLong(t[0]);
        long r = t.length > 1 ? potencia(base, Integer.parseInt(t[1])) : potencia(base);
        System.out.println("resultado=" + r);
    }
}
