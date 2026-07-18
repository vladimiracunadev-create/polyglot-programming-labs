use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let x = n;
    {
        let x = n + 10; // sombreado idiomático en Rust
        println!("interno={x} externo={n}");
    }
    let _ = x;
}
