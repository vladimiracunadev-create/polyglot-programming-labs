import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Map<String, String> almacen = new HashMap<>();
        almacen.put(p[0], p[1]);
        System.out.println("guardado=" + p[0] + "=" + almacen.get(p[0]));
    }
}
