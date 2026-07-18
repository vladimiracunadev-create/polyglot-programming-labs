import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<String> l = new ArrayList<>();
        for (String s : p) l.add(s);
        List<String> rev = new ArrayList<>(l);
        java.util.Collections.reverse(rev);
        System.out.println("pila=" + String.join("-", rev) + " cola=" + String.join("-", l));
    }
}
