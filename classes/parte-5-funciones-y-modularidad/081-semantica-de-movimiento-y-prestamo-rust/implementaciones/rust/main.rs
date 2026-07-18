use std::io::Read;

fn longitud(s: &str) -> usize {
    s.len() // préstamo: se lee sin tomar la propiedad
}

fn mostrar(s: String) {
    // move: 'mostrar' se vuelve dueña de la cadena
    let len = s.len();
    println!("movido={s} longitud={len}");
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).unwrap();
    let s = buf.trim().to_string();
    let _ = longitud(&s); // se presta
    mostrar(s); // se mueve
}
