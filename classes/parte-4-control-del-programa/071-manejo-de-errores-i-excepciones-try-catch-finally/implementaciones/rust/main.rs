use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let (a, b) = (v[0], v[1]);
    // Rust no usa excepciones: checked_div devuelve Option.
    match a.checked_div(b) {
        Some(r) => println!("resultado={r}"),
        None => println!("error=division por cero"),
    }
}
