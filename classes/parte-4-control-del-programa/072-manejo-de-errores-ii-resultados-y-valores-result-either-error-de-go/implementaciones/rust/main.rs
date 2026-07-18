use std::io::Read;

fn dividir(a: i64, b: i64) -> Result<i64, String> {
    if b == 0 {
        Err("division".to_string())
    } else {
        Ok(a / b)
    }
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    match dividir(v[0], v[1]) {
        Ok(r) => println!("ok={r}"),
        Err(e) => println!("err={e}"),
    }
}
