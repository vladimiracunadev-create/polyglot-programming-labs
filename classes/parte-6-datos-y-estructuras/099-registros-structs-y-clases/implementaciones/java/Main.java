import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    record Persona(String nombre, int edad) {}

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Persona p = new Persona(t[0], Integer.parseInt(t[1]));
        System.out.println("Persona(nombre=" + p.nombre() + ", edad=" + p.edad() + ")");
    }
}
