use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut d = 2;
    while d <= n {
        if n % d == 0 {
            break;
        }
        d += 1;
    }
    println!("primer_divisor={d}");
}
