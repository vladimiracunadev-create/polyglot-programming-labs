use std::io::Read;

struct Contador {
    cuenta: i64,
}

impl Contador {
    fn nuevo() -> Self {
        Contador { cuenta: 0 }
    }
    fn incrementar(&mut self) {
        self.cuenta += 1;
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut c = Contador::nuevo();
    for _ in 0..n {
        c.incrementar();
    }
    println!("cuenta={}", c.cuenta);
}
