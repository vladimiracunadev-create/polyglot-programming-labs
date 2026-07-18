import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    interface Forma { long area(); }
    static class Cuadrado implements Forma {
        long l; Cuadrado(long l) { this.l = l; }
        public long area() { return l * l; }
    }
    static class Rectangulo implements Forma {
        long a, b; Rectangulo(long a, long b) { this.a = a; this.b = b; }
        public long area() { return a * b; }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Forma f = t[0].equals("cuadrado")
                ? new Cuadrado(Long.parseLong(t[1]))
                : new Rectangulo(Long.parseLong(t[1]), Long.parseLong(t[2]));
        System.out.println("area=" + f.area());
    }
}
