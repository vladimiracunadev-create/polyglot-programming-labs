use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<&str> = s.split_whitespace().collect();
    let mut rev = nums.clone();
    rev.reverse();
    println!("pila={} cola={}", rev.join("-"), nums.join("-"));
}
