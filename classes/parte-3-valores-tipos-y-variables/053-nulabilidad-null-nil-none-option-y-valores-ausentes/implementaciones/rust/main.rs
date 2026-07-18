use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let valor: Option<i64> = if n == 0 { None } else { Some(n) };
    match valor {
        None => println!("valor=ausente"),
        Some(v) => println!("valor={v}"),
    }
}
