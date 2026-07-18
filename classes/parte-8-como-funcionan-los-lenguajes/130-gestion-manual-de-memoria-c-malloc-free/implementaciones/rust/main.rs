use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let arr: Vec<i64> = (1..=n).collect(); // Vec libera al salir del ámbito
    let suma: i64 = arr.iter().sum();
    println!("reservado={n} suma={suma}");
}
