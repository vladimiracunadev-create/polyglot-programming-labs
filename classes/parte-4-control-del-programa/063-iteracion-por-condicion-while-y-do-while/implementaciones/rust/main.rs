use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut suma = 0i64;
    let mut i = 1i64;
    while i <= n {
        suma += i;
        i += 1;
    }
    println!("suma={suma}");
}
