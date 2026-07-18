use std::io::Read;

struct Obj {
    valor: i64,
}

impl Obj {
    fn doble(&self) -> i64 {
        self.valor * 2
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let o = Obj { valor: n };
    println!("resultado={}", o.doble());
}
