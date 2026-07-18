use std::io::Read;

fn cuadrado(n: i64) -> i64 {
    n * n
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("puro={}", cuadrado(n));
}
