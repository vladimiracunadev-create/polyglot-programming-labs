import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] msgs = br.readLine().trim().split("\\s+");
        System.out.println("commits=" + msgs.length);
    }
}
