use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut cuenta = 0;
    for _ in s.split_whitespace() {
        cuenta += 1;
    }
    println!("cuenta={cuenta}");
}
