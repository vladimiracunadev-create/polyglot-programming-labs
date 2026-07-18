use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let (viejo, nuevo) = (n * 2, n + n);
    let eq = if viejo == nuevo { "true" } else { "false" };
    println!("equivalente={eq} resultado={nuevo}");
}
