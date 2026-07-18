use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pares: Vec<String> = (1..=n).map(|i| (2 * i).to_string()).collect();
    println!("pares={}", pares.join("-"));
}
