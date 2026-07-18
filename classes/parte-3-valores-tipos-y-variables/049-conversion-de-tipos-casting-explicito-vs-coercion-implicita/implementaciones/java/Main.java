import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        double f = Double.parseDouble(br.readLine().trim());
        System.out.printf(Locale.US, "entero=%d real=%.2f%n", (long) f, f);
    }
}
