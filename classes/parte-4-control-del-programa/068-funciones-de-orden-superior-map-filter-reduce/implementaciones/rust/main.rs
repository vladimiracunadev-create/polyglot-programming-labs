use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let doblados: Vec<i64> = s
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap() * 2)
        .collect();
    let total: i64 = doblados.iter().sum();
    let texto: Vec<String> = doblados.iter().map(|x| x.to_string()).collect();
    println!("doblados={} total={}", texto.join("-"), total);
}
