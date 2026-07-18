use std::io::Read;

trait Animal {
    fn sonido(&self) -> &'static str;
}

struct Perro;
struct Gato;
struct Vaca;

impl Animal for Perro { fn sonido(&self) -> &'static str { "guau" } }
impl Animal for Gato { fn sonido(&self) -> &'static str { "miau" } }
impl Animal for Vaca { fn sonido(&self) -> &'static str { "muu" } }

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let tipo = s.trim();
    let a: Box<dyn Animal> = match tipo {
        "perro" => Box::new(Perro),
        "gato" => Box::new(Gato),
        _ => Box::new(Vaca),
    };
    println!("sonido={}", a.sonido());
}
