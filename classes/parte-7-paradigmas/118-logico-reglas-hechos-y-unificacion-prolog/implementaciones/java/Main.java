import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static boolean esDivisor(long a, long b) {
        return b % a == 0;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(p[0]);
        long b = Long.parseLong(p[1]);
        System.out.println("divisor=" + (esDivisor(a, b) ? "true" : "false"));
    }
}
