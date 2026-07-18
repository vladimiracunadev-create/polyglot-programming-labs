use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let set: HashSet<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("unicos={}", set.len());
}
