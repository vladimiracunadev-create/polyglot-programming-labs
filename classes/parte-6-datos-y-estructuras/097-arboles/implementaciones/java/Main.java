import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.TreeSet;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        TreeSet<Integer> t = new TreeSet<>();
        for (String s : p) t.add(Integer.parseInt(s));
        System.out.println("inorden=" + t.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
