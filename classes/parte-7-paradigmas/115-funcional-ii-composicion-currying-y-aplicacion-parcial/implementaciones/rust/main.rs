use std::io::Read;

fn doblar(x: i64) -> i64 {
    x * 2
}

fn incrementar(x: i64) -> i64 {
    x + 1
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", incrementar(doblar(n)));
}
