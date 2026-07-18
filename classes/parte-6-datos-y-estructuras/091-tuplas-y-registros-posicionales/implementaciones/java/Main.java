import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Par(int a, int b) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Par t = new Par(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        Par s = new Par(t.b(), t.a());
        System.out.println("tupla=(" + s.a() + ", " + s.b() + ")");
    }
}
