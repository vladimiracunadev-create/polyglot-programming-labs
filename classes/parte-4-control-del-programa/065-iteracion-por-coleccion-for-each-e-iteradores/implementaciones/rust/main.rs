use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut suma = 0i64;
    for x in &nums {
        suma += x;
    }
    println!("suma={suma}");
}
