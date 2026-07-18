import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Contador {
        int cuenta = 0;
        void incrementar() { cuenta++; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        Contador c = new Contador();
        for (int i = 0; i < n; i++) c.incrementar();
        System.out.println("cuenta=" + c.cuenta);
    }
}
