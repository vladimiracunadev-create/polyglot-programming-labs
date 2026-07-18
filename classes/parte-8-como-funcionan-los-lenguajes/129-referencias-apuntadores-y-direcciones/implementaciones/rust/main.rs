use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let indice: usize = t[0].parse().unwrap();
    let lista = &t[1..];
    println!("valor={}", lista[indice]);
}
