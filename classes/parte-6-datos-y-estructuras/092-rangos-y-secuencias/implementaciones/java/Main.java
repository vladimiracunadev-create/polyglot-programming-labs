import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        StringBuilder sb = new StringBuilder();
        long suma = 0;
        for (int i = a; i <= b; i++) {
            if (i > a) sb.append("-");
            sb.append(i);
            suma += i;
        }
        System.out.println("rango=" + sb + " suma=" + suma);
    }
}
