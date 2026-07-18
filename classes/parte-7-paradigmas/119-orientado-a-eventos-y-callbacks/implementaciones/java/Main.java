import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.function.IntConsumer;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        List<Integer> recolectados = new ArrayList<>();
        IntConsumer alEvento = recolectados::add;
        for (int i = 1; i <= n; i++) alEvento.accept(i);
        System.out.println("eventos=" + recolectados.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
