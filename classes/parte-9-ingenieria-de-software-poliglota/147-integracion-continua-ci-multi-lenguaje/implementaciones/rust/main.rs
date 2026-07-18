use std::io::Read;

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let verde = s.split_whitespace().all(|x| x.parse::<i64>().unwrap() == 1);
    println!("ci={}", if verde { "verde" } else { "rojo" });
}
