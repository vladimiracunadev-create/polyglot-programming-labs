import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    static class Cuenta {
        private long saldo = 0;

        void depositar(long monto) {
            saldo += monto;
        }

        long saldo() {
            return saldo;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        Cuenta c = new Cuenta();
        c.depositar(n);
        c.depositar(n);
        System.out.println("saldo=" + c.saldo());
    }
}
