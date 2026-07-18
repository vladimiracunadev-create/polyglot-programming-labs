import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntUnaryOperator;

public class Main {
    static IntUnaryOperator hacerSumador(int base) {
        return x -> base + x; // captura base (efectivamente final)
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int base = Integer.parseInt(br.readLine().trim());
        IntUnaryOperator sumar = hacerSumador(base);
        System.out.println("r1=" + sumar.applyAsInt(1) + " r2=" + sumar.applyAsInt(2));
    }
}
