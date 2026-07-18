use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.trim().split('.').map(|x| x.parse().unwrap()).collect();
    println!("mayor={} menor={} parche={}", v[0], v[1], v[2]);
}
