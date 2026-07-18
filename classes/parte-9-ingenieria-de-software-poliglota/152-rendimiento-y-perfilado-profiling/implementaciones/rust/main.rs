use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut ops = 0i64;
    let mut suma = 0i64;
    for i in 1..=n {
        suma += i;
        ops += 1;
    }
    println!("operaciones={ops} resultado={suma}");
}
