use std::io::Read;

struct Persona {
    nombre: String,
    edad: i64,
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let t: Vec<&str> = s.split_whitespace().collect();
    let p = Persona {
        nombre: t[0].to_string(),
        edad: t[1].parse().unwrap(),
    };
    println!("Persona(nombre={}, edad={})", p.nombre, p.edad);
}
