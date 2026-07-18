use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let c = s.chars().next().unwrap();
    println!("char={} codigo={}", c, c as u32);
}
