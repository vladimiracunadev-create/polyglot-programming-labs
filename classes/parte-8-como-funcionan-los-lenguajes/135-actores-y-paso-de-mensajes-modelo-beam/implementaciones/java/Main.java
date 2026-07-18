import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Acumulador {
        long total = 0;
        void recibir(int m) { total += m; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Acumulador actor = new Acumulador();
        for (String s : p) actor.recibir(Integer.parseInt(s));
        System.out.println("total=" + actor.total);
    }
}
