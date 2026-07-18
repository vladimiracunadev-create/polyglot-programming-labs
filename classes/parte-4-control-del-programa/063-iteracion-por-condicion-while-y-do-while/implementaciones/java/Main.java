import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        long suma = 0;
        int i = 1;
        while (i <= n) {
            suma += i;
            i++;
        }
        System.out.println("suma=" + suma);
    }
}
