import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        System.out.printf("dec=%d hex=%s oct=%s bin=%s%n", n,
                Integer.toHexString(n), Integer.toOctalString(n), Integer.toBinaryString(n));
    }
}
