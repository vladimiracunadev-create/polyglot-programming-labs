use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let inv: String = w.chars().rev().collect();
    println!("invertido={inv}");
}
