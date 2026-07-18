use std::io::Read;

fn suma(nums: &[i64]) -> i64 {
    nums.iter().sum()
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={}", suma(&nums));
}
