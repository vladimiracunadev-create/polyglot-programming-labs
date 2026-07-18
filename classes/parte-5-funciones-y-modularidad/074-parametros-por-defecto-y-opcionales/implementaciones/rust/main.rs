use std::io::Read;

fn potencia(base: i64, exp: u32) -> i64 {
    base.pow(exp)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let base: i64 = t[0].parse().unwrap();
    let exp: u32 = if t.len() > 1 { t[1].parse().unwrap() } else { 2 };
    println!("resultado={}", potencia(base, exp));
}
