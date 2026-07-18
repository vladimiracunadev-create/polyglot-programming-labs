import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int d = Integer.parseInt(br.readLine().trim());
        String dia;
        switch (d) {
            case 1: dia = "lunes"; break;
            case 2: dia = "martes"; break;
            case 3: dia = "miercoles"; break;
            case 4: dia = "jueves"; break;
            case 5: dia = "viernes"; break;
            case 6: dia = "sabado"; break;
            case 7: dia = "domingo"; break;
            default: dia = "invalido";
        }
        System.out.println("dia=" + dia);
    }
}
