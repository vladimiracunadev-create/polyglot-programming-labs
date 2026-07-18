import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntBinaryOperator;

public class Main {
    static int aplicar(IntBinaryOperator f, int a, int b) {
        return f.applyAsInt(a, b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        IntBinaryOperator suma = (x, y) -> x + y;
        IntBinaryOperator producto = (x, y) -> x * y;
        System.out.println("suma=" + aplicar(suma, a, b) + " producto=" + aplicar(producto, a, b));
    }
}
