import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        List<Integer> nums = new ArrayList<>();
        for (String s : p) nums.add(Integer.parseInt(s));
        Collections.reverse(nums);
        System.out.println("invertido=" + nums.stream().map(String::valueOf).collect(Collectors.joining("-")));
    }
}
