use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let r: Vec<i64> = (v[0]..=v[1]).collect();
    let suma: i64 = r.iter().sum();
    let texto: Vec<String> = r.iter().map(|x| x.to_string()).collect();
    println!("rango={} suma={}", texto.join("-"), suma);
}
