use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let a: i64 = t[1].parse().unwrap();
    let b: i64 = t[2].parse().unwrap();
    let r = match t[0] {
        "suma" => a + b,
        "resta" => a - b,
        _ => a * b,
    };
    println!("resultado={r}");
}
