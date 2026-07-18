use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let doblados: Vec<String> = s
        .split_whitespace()
        .map(|x| (x.parse::<i64>().unwrap() * 2).to_string())
        .collect();
    println!("doblados={}", doblados.join("-"));
}
