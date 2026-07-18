use std::io::Read;

fn tf(x: bool) -> &'static str {
    if x { "true" } else { "false" }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let pos = n > 0;
    let par = n % 2 == 0;
    println!("positivo={} par={} ambos={}", tf(pos), tf(par), tf(pos && par));
}
