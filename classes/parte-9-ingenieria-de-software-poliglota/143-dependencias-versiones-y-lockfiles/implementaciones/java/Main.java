import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] v = br.readLine().trim().split("\\.");
        System.out.println("mayor=" + Integer.parseInt(v[0]) + " menor=" + Integer.parseInt(v[1]) + " parche=" + Integer.parseInt(v[2]));
    }
}
