import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static String tf(boolean x) {
        return x ? "true" : "false";
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean a = Integer.parseInt(p[0]) != 0;
        boolean b = Integer.parseInt(p[1]) != 0;
        System.out.printf("and=%s or=%s not_a=%s%n", tf(a && b), tf(a || b), tf(!a));
    }
}
