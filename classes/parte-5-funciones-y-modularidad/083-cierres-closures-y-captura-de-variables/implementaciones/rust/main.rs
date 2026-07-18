use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let base: i64 = s.trim().parse().unwrap();
    let sumar = |x: i64| base + x; // captura base
    println!("r1={} r2={}", sumar(1), sumar(2));
}
