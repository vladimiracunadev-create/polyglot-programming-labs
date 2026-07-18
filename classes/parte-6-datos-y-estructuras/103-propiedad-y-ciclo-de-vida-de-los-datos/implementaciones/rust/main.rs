use std::io::Read;

struct Recurso {
    valor: i64,
}

impl Drop for Recurso {
    fn drop(&mut self) {
        // se libera automáticamente al salir del ámbito
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let valor;
    {
        let r = Recurso { valor: n };
        valor = r.valor;
    } // aquí se ejecuta Drop
    println!("valor={valor} estado=liberado");
}
