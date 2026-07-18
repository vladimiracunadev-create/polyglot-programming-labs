use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    nums.sort();
    let texto: Vec<String> = nums.iter().map(|x| x.to_string()).collect();
    println!("inorden={}", texto.join("-"));
}
