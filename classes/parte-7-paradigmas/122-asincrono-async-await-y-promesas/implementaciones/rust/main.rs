use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    // Sin runtime async externo, se muestra el resultado de la tarea.
    let resultado = n * 2;
    println!("resultado={resultado}");
}
