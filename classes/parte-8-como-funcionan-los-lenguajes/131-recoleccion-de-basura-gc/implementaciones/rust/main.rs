use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    for _ in 0..n {
        let _tmp = Box::new(0); // se libera al salir del ámbito (sin GC)
    }
    println!("creados={n} estado=recolectado");
}
