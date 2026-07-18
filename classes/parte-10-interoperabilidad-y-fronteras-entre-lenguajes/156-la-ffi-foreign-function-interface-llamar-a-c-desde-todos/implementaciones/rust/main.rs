use std::io::Read;

fn doble(x: i64) -> i64 {
    x * 2 // en un caso real, una funcion externa con extern "C"
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    println!("resultado={}", doble(n));
}
