use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let f: f64 = s.trim().parse().unwrap();
    println!("entero={} real={:.2}", f as i64, f);
}
