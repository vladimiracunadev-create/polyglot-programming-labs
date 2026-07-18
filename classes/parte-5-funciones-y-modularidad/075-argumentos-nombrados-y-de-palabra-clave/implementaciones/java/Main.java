import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java no tiene argumentos nombrados: se pasan por posición.
    static String punto(int x, int y) {
        return "punto(x=" + x + ", y=" + y + ")";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        System.out.println(punto(Integer.parseInt(p[0]), Integer.parseInt(p[1])));
    }
}
