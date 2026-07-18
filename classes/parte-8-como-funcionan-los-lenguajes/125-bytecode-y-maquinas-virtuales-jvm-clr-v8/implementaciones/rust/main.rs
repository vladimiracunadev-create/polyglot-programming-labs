use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let mut pila: Vec<i64> = vec![t[0].parse().unwrap(), t[1].parse().unwrap()];
    let y = pila.pop().unwrap();
    let x = pila.pop().unwrap();
    let r = match t[2] {
        "+" => x + y,
        "-" => x - y,
        _ => x * y,
    };
    println!("resultado={r}");
}
