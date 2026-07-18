use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let signo = match n {
        n if n > 0 => "positivo",
        n if n < 0 => "negativo",
        _ => "cero",
    };
    println!("signo={signo}");
}
