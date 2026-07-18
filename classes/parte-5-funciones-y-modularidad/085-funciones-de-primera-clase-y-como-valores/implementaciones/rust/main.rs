use std::io::Read;

fn suma(a: i64, b: i64) -> i64 {
    a + b
}

fn producto(a: i64, b: i64) -> i64 {
    a * b
}

fn aplicar(f: fn(i64, i64) -> i64, a: i64, b: i64) -> i64 {
    f(a, b)
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    println!("suma={} producto={}", aplicar(suma, v[0], v[1]), aplicar(producto, v[0], v[1]));
}
