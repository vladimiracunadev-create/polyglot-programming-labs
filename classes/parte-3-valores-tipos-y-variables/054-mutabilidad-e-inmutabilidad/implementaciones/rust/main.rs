use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let parts: Vec<String> = (1..=n).map(|i| i.to_string()).collect();
    println!("sec={}", parts.join("-"));
}
