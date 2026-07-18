use std::io::Read;
use std::sync::Mutex;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let cuenta = Mutex::new(0i64);
    for _ in 0..n {
        *cuenta.lock().unwrap() += 1;
    }
    println!("cuenta={}", *cuenta.lock().unwrap());
}
