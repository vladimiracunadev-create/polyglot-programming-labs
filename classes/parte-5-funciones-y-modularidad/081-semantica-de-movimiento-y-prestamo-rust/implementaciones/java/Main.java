import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine().trim();
        int longitud = s.length(); // GC: sin propiedad ni move.
        System.out.println("movido=" + s + " longitud=" + longitud);
    }
}
