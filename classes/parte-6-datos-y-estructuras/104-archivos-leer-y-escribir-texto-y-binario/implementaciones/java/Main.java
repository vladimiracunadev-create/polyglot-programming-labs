import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String linea = br.readLine();
        int palabras = linea.trim().isEmpty() ? 0 : linea.trim().split("\\s+").length;
        System.out.println("palabras=" + palabras + " caracteres=" + linea.length());
    }
}
