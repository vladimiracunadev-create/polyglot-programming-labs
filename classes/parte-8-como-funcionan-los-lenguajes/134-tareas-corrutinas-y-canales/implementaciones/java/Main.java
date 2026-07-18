import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int maximo = Integer.parseInt(p[0]);
        for (String s : p) maximo = Math.max(maximo, Integer.parseInt(s));
        System.out.println("max=" + maximo);
    }
}
