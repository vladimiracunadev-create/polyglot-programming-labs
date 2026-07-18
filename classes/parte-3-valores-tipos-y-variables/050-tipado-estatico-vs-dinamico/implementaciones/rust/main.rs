use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = v[0].parse().unwrap();
    let b: f64 = v[1].parse().unwrap();
    println!("suma={:.2}", a as f64 + b);
}
