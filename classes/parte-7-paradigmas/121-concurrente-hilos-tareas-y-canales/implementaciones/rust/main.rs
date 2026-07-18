use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let medio = nums.len() / 2;
    let p1: i64 = nums[..medio].iter().sum();
    let p2: i64 = nums[medio..].iter().sum();
    println!("suma={}", p1 + p2);
}
