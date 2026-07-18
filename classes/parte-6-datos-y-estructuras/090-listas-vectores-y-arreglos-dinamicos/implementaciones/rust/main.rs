use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<&str> = s.split_whitespace().collect();
    nums.reverse();
    println!("invertido={}", nums.join("-"));
}
