import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long ops = 0, suma = 0;
        for (int i = 1; i <= n; i++) {
            suma += i;
            ops += 1;
        }
        System.out.println("operaciones=" + ops + " resultado=" + suma);
    }
}
