import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        Optional<Integer> opcion = n > 0 ? Optional.of(n) : Optional.empty();
        Optional<Integer> r = opcion.map(x -> x * 2);
        System.out.println(r.map(x -> "resultado=" + x).orElse("resultado=nada"));
    }
}
