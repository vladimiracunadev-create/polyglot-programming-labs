use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: u32 = s.trim().parse().unwrap();
    let r: i64 = 2i64.pow(n);
    println!("resultado={r}");
}
