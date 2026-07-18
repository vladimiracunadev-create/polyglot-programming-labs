use std::io::Read;

fn main() {
    let mut entrada = String::new();
    std::io::stdin().read_to_string(&mut entrada).unwrap();
    let campos: Vec<&str> = entrada.split_whitespace().collect();

    // Rust: inmutable por defecto (`let`), tipos explícitos, conversión con `as`.
    let precio_unitario: f64 = campos[0].parse().unwrap();
    let cantidad: i64 = campos[1].parse().unwrap();
    let descuento: f64 = campos[2].parse().unwrap();

    let subtotal = precio_unitario * cantidad as f64;
    let total = subtotal * (1.0 - descuento);

    println!("Total: {total:.2}");
}
