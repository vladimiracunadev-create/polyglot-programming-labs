use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let stream: Vec<String> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .filter(|x| x % 2 == 0)
        .map(|x| (x * 2).to_string())
        .collect();
    println!("stream={}", stream.join("-"));
}
