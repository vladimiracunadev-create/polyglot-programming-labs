import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        List<Integer> lista = new ArrayList<>();
        for (int i = n; i >= 1; i--) lista.add(i);
        System.out.println("lista=" + lista.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
