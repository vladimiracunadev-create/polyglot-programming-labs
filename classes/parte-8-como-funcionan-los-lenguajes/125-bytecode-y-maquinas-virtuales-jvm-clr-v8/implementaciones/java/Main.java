import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] t = br.readLine().trim().split("\\s+");
        Deque<Long> pila = new ArrayDeque<>();
        pila.push(Long.parseLong(t[0]));
        pila.push(Long.parseLong(t[1]));
        long y = pila.pop(), x = pila.pop();
        long r = t[2].equals("+") ? x + y : t[2].equals("-") ? x - y : x * y;
        System.out.println("resultado=" + r);
    }
}
