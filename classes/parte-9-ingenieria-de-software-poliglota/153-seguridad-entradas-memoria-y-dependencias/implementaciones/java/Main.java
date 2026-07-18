import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String w = br.readLine().trim();
        boolean seguro = w.matches("[A-Za-z0-9]+");
        System.out.println("seguro=" + (seguro ? "true" : "false"));
    }
}
