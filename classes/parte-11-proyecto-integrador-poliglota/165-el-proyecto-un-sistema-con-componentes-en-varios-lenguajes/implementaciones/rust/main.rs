use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c: Vec<&str> = s.split_whitespace().collect();
    println!("componentes={} nombres={}", c.len(), c.join("-"));
}
