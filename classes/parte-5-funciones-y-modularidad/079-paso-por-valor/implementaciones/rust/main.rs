use std::io::Read;

fn doblar(mut x: i64) -> i64 {
    x *= 2;
    x
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let local = doblar(n);
    println!("original={n} local={local}");
}
