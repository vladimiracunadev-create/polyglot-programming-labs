import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static String tf(boolean x) {
        return x ? "true" : "false";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        boolean pos = n > 0;
        boolean par = n % 2 == 0;
        System.out.printf("positivo=%s par=%s ambos=%s%n", tf(pos), tf(par), tf(pos && par));
    }
}
