use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let nombre = t[0];
    let edad: i64 = t[1].parse().unwrap();
    println!("{{\"nombre\": \"{nombre}\", \"edad\": {edad}}}");
}
