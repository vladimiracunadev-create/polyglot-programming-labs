import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        boolean verde = true;
        for (String s : p) if (Integer.parseInt(s) != 1) verde = false;
        System.out.println("ci=" + (verde ? "verde" : "rojo"));
    }
}
