import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] p = br.readLine().trim().split("\\s+");
        int[] nums = new int[p.length];
        for (int i = 0; i < p.length; i++) nums[i] = Integer.parseInt(p[i]);
        int medio = nums.length / 2;
        long p1 = 0, p2 = 0;
        for (int i = 0; i < medio; i++) p1 += nums[i];
        for (int i = medio; i < nums.length; i++) p2 += nums[i];
        System.out.println("suma=" + (p1 + p2));
    }
}
