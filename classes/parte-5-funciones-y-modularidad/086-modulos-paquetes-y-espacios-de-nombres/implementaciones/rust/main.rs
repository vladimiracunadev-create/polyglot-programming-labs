use std::io::Read;

mod matematicas {
    pub fn doble(n: i64) -> i64 {
        2 * n
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", matematicas::doble(n));
}
