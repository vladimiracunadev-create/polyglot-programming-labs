import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nums = br.readLine().trim().split("\\s+");
        int cuenta = 0;
        for (String s : nums) cuenta += 1;
        System.out.println("cuenta=" + cuenta);
    }
}
