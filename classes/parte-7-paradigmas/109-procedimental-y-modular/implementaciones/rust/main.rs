use std::io::Read;

fn promedio(a: &[i64]) -> i64 {
    let suma: i64 = a.iter().sum();
    suma / a.len() as i64
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("promedio={}", promedio(&nums));
}
