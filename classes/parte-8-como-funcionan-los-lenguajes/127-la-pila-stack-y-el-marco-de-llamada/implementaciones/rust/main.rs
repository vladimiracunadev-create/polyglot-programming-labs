use std::io::Read;

fn sumar(n: i64) -> i64 {
    if n == 0 {
        0
    } else {
        n + sumar(n - 1)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("suma={} profundidad={}", sumar(n), n);
}
