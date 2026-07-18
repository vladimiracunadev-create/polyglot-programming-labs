use std::io::Read;

struct Cuenta {
    saldo: i64, // privado fuera del módulo
}

impl Cuenta {
    fn nueva() -> Self {
        Cuenta { saldo: 0 }
    }
    fn depositar(&mut self, monto: i64) {
        self.saldo += monto;
    }
    fn saldo(&self) -> i64 {
        self.saldo
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut c = Cuenta::nueva();
    c.depositar(n);
    c.depositar(n);
    println!("saldo={}", c.saldo());
}
