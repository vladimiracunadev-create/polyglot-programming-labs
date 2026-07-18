import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int d = 2;
        for (; d <= n; d++) {
            if (n % d == 0) break;
        }
        System.out.println("primer_divisor=" + d);
    }
}
