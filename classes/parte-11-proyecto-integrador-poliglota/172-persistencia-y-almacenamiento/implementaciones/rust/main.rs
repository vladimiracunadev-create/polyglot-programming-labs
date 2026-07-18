use std::collections::HashMap;
use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let p: Vec<&str> = s.split_whitespace().collect();
    let mut almacen: HashMap<&str, &str> = HashMap::new();
    almacen.insert(p[0], p[1]);
    println!("guardado={}={}", p[0], almacen[p[0]]);
}
