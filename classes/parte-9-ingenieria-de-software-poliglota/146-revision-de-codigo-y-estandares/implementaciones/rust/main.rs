use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let w = s.trim();
    let valido = !w.is_empty() && w.chars().all(|c| c.is_ascii_lowercase());
    println!("valido={}", if valido { "true" } else { "false" });
}
