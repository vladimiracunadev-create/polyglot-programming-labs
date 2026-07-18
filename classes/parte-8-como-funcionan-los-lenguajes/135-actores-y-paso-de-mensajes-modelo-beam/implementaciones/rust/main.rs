use std::io::Read;

struct Acumulador {
    total: i64,
}

impl Acumulador {
    fn recibir(&mut self, mensaje: i64) {
        self.total += mensaje;
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let mut actor = Acumulador { total: 0 };
    for x in s.split_whitespace() {
        actor.recibir(x.parse().unwrap());
    }
    println!("total={}", actor.total);
}
