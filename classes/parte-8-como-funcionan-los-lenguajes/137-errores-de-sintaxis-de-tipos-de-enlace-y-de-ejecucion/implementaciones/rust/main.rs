use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let codigo: i64 = s.trim().parse().unwrap();
    let e = match codigo {
        1 => "sintaxis",
        2 => "tipos",
        3 => "enlace",
        4 => "ejecucion",
        _ => "desconocido",
    };
    println!("error={e}");
}
