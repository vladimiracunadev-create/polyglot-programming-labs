use std::io::Read;

fn join(a: &[i64]) -> String {
    a.iter().map(|x| x.to_string()).collect::<Vec<_>>().join("-")
}

fn main() {
    let mut s = String::new();
    std::io::stdin().read_to_string(&mut s).unwrap();
    let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
    let mut copia = nums.clone();
    let n = copia.len();
    copia[n - 1] = 99;
    println!("original={} copia={}", join(&nums), join(&copia));
}
