import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int codigo = Integer.parseInt(br.readLine().trim());
        String e;
        switch (codigo) {
            case 1: e = "sintaxis"; break;
            case 2: e = "tipos"; break;
            case 3: e = "enlace"; break;
            case 4: e = "ejecucion"; break;
            default: e = "desconocido";
        }
        System.out.println("error=" + e);
    }
}
