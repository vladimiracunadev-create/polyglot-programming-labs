use std::io::Read;

fn punto(x: i64, y: i64) -> String {
    format!("punto(x={x}, y={y})")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("{}", punto(v[0], v[1]));
}
