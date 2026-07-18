use std::io::Read;

fn doble(x: i64) -> i64 {
    x * 2
}

fn wrapper(x: i64) -> String {
    format!("wrap({})", doble(x))
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("envuelto={}", wrapper(n));
}
