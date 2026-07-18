import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.function.IntUnaryOperator;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        IntUnaryOperator doblar = x -> x * 2;
        IntUnaryOperator incrementar = x -> x + 1;
        IntUnaryOperator compuesta = doblar.andThen(incrementar);
        System.out.println("resultado=" + compuesta.applyAsInt(n));
    }
}
