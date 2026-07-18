import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        for (int i = 0; i < n; i++) {
            Object tmp = new Object(); // el GC lo recolectará
            if (tmp == null) return;
        }
        System.out.println("creados=" + n + " estado=recolectado");
    }
}
