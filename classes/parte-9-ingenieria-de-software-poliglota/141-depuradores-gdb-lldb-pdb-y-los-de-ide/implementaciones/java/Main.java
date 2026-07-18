import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long acc = 0;
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            acc += i;
            if (i > 1) sb.append("-");
            sb.append(acc);
        }
        System.out.println("traza=" + sb);
    }
}
