use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let edad: i64 = s.trim().parse().unwrap();
    if edad < 0 {
        println!("invalido");
    } else if edad < 18 {
        println!("menor");
    } else {
        println!("adulto");
    }
}
