use std::io::Read;

fn doble(x: &i64) -> i64 {
    *x * 2 // préstamo: se lee sin tomar la propiedad
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", doble(&n));
}
