import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String par = (n % 2 == 0) ? "true" : "false";
        System.out.printf(Locale.US, "entero=%d real=%.1f par=%s%n", n, (double) n, par);
    }
}
