import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.Set;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Set<Integer> nodos = new HashSet<>();
        for (String s : p) nodos.add(Integer.parseInt(s));
        System.out.println("aristas=" + (p.length / 2) + " nodos=" + nodos.size());
    }
}
