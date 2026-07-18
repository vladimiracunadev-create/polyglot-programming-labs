use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let lista: Vec<String> = (1..=n).rev().map(|x| x.to_string()).collect();
    println!("lista={}", lista.join("-"));
}
