import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String tipo = br.readLine().trim();
        String r;
        switch (tipo) {
            case "sistemas": r = "Rust"; break;
            case "web": r = "TypeScript"; break;
            case "datos": r = "SQL"; break;
            default: r = "Python";
        }
        System.out.println("lenguaje=" + r);
    }
}
