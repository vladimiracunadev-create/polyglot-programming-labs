import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        String r = Arrays.stream(p).map(Integer::parseInt).map(x -> x * 2)
                .map(String::valueOf).collect(Collectors.joining("-"));
        System.out.println("doblados=" + r);
    }
}
