use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut acc = 0i64;
    let mut pasos: Vec<String> = Vec::new();
    for i in 1..=n {
        acc += i;
        pasos.push(acc.to_string());
    }
    println!("traza={}", pasos.join("-"));
}
