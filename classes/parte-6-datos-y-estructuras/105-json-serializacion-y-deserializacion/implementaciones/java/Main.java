import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        String nombre = t[0];
        int edad = Integer.parseInt(t[1]);
        System.out.println("{\"nombre\": \"" + nombre + "\", \"edad\": " + edad + "}");
    }
}
