use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let par = if n % 2 == 0 { "true" } else { "false" };
    println!("entero={n} real={:.1} par={par}", n as f64);
}
