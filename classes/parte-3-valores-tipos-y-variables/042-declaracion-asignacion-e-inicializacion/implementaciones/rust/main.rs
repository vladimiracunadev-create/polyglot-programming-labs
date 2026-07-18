use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();

    // Intercambio por desestructuración de tupla.
    let (a, b) = (v[1], v[0]);

    println!("a={a} b={b}");
}
