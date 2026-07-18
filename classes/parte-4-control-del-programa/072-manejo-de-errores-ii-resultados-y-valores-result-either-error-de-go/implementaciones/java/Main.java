import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Optional;

public class Main {
    static Optional<Integer> dividir(int a, int b) {
        return b == 0 ? Optional.empty() : Optional.of(a / b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int a = Integer.parseInt(p[0]);
        int b = Integer.parseInt(p[1]);
        Optional<Integer> r = dividir(a, b);
        System.out.println(r.isPresent() ? "ok=" + r.get() : "err=division");
    }
}
