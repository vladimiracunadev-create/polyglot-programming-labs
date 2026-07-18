use std::io::Read;

enum Forma {
    Cuadrado(i64),
    Rectangulo(i64, i64),
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let forma = if t[0] == "cuadrado" {
        Forma::Cuadrado(t[1].parse().unwrap())
    } else {
        Forma::Rectangulo(t[1].parse().unwrap(), t[2].parse().unwrap())
    };
    let area = match forma {
        Forma::Cuadrado(l) => l * l,
        Forma::Rectangulo(a, b) => a * b,
    };
    println!("area={area}");
}
