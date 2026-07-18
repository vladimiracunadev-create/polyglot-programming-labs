import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    interface Animal { String sonido(); }
    static class Perro implements Animal { public String sonido() { return "guau"; } }
    static class Gato implements Animal { public String sonido() { return "miau"; } }
    static class Vaca implements Animal { public String sonido() { return "muu"; } }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String tipo = br.readLine().trim();
        Animal a;
        switch (tipo) {
            case "perro": a = new Perro(); break;
            case "gato": a = new Gato(); break;
            default: a = new Vaca();
        }
        System.out.println("sonido=" + a.sonido());
    }
}
