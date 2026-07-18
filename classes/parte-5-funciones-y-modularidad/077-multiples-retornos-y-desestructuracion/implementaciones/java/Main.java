import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    // Java devuelve un objeto (record) para varios valores.
    record DivRes(int cociente, int resto) {}

    static DivRes divmod(int a, int b) {
        return new DivRes(a / b, a % b);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        DivRes d = divmod(Integer.parseInt(p[0]), Integer.parseInt(p[1]));
        System.out.println("cociente=" + d.cociente() + " resto=" + d.resto());
    }
}
