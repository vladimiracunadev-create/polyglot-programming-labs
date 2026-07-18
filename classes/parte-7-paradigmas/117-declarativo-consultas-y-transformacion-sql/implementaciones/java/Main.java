import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        long suma = Arrays.stream(p).mapToInt(Integer::parseInt).filter(x -> x % 2 == 0).sum();
        System.out.println("suma_pares=" + suma);
    }
}
