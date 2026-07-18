import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String t = Integer.toString(n) + Integer.toString(n);
        System.out.printf("suma=%d texto=%s%n", n + n, t);
    }
}
