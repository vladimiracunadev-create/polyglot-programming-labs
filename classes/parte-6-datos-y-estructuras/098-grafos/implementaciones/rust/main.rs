use std::collections::HashSet;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let aristas = nums.len() / 2;
    let nodos: HashSet<i64> = nums.iter().copied().collect();
    println!("aristas={} nodos={}", aristas, nodos.len());
}
