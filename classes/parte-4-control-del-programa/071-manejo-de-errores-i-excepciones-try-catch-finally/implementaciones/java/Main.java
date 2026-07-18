import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        try {
            int r = a / b;
            System.out.println("resultado=" + r);
        } catch (ArithmeticException e) {
            System.out.println("error=division por cero");
        }
    }
}
