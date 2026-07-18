use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let linea = s.trim_end_matches(['\r', '\n']);
    println!("eco: {linea}");
}
