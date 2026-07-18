import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        Map<Integer, Integer> freq = new HashMap<>();
        for (String s : p) {
            int x = Integer.parseInt(s);
            freq.merge(x, 1, Integer::sum);
        }
        System.out.println("cuenta=" + freq.get(Integer.parseInt(p[0])));
    }
}
