use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let opcion: Option<i64> = if n > 0 { Some(n) } else { None };
    match opcion.map(|x| x * 2) {
        Some(r) => println!("resultado={r}"),
        None => println!("resultado=nada"),
    }
}
