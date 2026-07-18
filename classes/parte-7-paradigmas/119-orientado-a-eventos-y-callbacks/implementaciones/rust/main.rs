use std::io::Read;

fn al_evento(recolectados: &mut Vec<String>, i: i64) {
    recolectados.push(i.to_string());
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let n: i64 = s.trim().parse().unwrap();
    let mut recolectados: Vec<String> = Vec::new();
    for i in 1..=n {
        al_evento(&mut recolectados, i);
    }
    println!("eventos={}", recolectados.join("-"));
}
