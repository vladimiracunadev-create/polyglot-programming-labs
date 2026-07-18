use std::io::Read;

fn doblar(x: &mut i64) {
    *x *= 2;
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut n: i64 = s.trim().parse().unwrap();
    let antes = n;
    doblar(&mut n);
    println!("antes={antes} despues={n}");
}
