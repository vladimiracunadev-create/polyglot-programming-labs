import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long a = Long.parseLong(t[0]), b = Long.parseLong(t[2]);
        long r = t[1].equals("+") ? a + b : t[1].equals("-") ? a - b : a * b;
        System.out.println("resultado=" + r);
    }
}
