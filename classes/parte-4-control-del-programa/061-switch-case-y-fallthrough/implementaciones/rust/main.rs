use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let d: i64 = s.trim().parse().unwrap();
    let dia = match d {
        1 => "lunes",
        2 => "martes",
        3 => "miercoles",
        4 => "jueves",
        5 => "viernes",
        6 => "sabado",
        7 => "domingo",
        _ => "invalido",
    };
    println!("dia={dia}");
}
