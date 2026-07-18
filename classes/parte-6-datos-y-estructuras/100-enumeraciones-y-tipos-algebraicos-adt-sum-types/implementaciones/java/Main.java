import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        long area;
        if (t[0].equals("cuadrado")) {
            long l = Long.parseLong(t[1]);
            area = l * l;
        } else {
            area = Long.parseLong(t[1]) * Long.parseLong(t[2]);
        }
        System.out.println("area=" + area);
    }
}
