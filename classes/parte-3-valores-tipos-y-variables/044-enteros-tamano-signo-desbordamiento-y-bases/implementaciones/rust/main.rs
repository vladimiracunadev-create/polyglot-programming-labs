use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: u64 = s.trim().parse().unwrap();
    println!("dec={n} hex={:x} oct={:o} bin={:b}", n, n, n);
}
