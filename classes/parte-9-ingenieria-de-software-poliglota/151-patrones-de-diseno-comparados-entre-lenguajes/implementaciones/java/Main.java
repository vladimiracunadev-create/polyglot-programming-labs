import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[1]), b = Long.parseLong(t[2]);
        long r;
        switch (t[0]) {
            case "suma": r = a + b; break;
            case "resta": r = a - b; break;
            default: r = a * b;
        }
        System.out.println("resultado=" + r);
    }
}
