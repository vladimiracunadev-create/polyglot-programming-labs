import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int score = Integer.parseInt(br.readLine().trim());
        String nota;
        if (score >= 90) nota = "A";
        else if (score >= 80) nota = "B";
        else if (score >= 70) nota = "C";
        else nota = "F";
        System.out.println("nota=" + nota);
    }
}
