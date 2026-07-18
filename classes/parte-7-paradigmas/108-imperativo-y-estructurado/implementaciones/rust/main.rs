use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut suma: i64 = 0;
    for x in s.split_whitespace() {
        suma += x.parse::<i64>().unwrap();
    }
    println!("suma={suma}");
}
