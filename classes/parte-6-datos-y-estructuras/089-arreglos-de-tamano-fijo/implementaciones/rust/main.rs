use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let arr: [i64; 3] = [v[0], v[1], v[2]];
    let suma: i64 = arr.iter().sum();
    let max = *arr.iter().max().unwrap();
    println!("suma={suma} max={max}");
}
