use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let recibido: i64 = s.split_whitespace().map(|x| x.parse::<i64>().unwrap()).sum();
    println!("recibido={recibido}");
}
