import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int edad = Integer.parseInt(br.readLine().trim());
        if (edad < 0) {
            System.out.println("invalido");
        } else if (edad < 18) {
            System.out.println("menor");
        } else {
            System.out.println("adulto");
        }
    }
}
