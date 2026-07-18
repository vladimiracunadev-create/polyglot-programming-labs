use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let v: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let t: (i64, i64) = (v[0], v[1]);
    let t = (t.1, t.0);
    println!("tupla=({}, {})", t.0, t.1);
}
