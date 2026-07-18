use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let tipo = s.trim();
    let r = match tipo {
        "sistemas" => "Rust",
        "web" => "TypeScript",
        "datos" => "SQL",
        _ => "Python",
    };
    println!("lenguaje={r}");
}
