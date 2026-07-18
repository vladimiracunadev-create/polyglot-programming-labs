use std::io::Read;

trait Forma {
    fn area(&self) -> i64;
}

struct Cuadrado(i64);
struct Rectangulo(i64, i64);

impl Forma for Cuadrado { fn area(&self) -> i64 { self.0 * self.0 } }
impl Forma for Rectangulo { fn area(&self) -> i64 { self.0 * self.1 } }

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let f: Box<dyn Forma> = if t[0] == "cuadrado" {
        Box::new(Cuadrado(t[1].parse().unwrap()))
    } else {
        Box::new(Rectangulo(t[1].parse().unwrap(), t[2].parse().unwrap()))
    };
    println!("area={}", f.area());
}
