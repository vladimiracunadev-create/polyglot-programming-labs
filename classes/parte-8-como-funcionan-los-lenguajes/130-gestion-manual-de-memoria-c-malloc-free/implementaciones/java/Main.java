import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        int[] arr = new int[n];
        long suma = 0;
        for (int i = 0; i < n; i++) {
            arr[i] = i + 1;
            suma += arr[i];
        }
        System.out.println("reservado=" + n + " suma=" + suma);
    }
}
