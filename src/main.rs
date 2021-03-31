use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let filename = "daily";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);

    /*
     * Todo List 
     * -----
     * 1. Find time between blocks
     * 2. For all time blocks, add that time to proper tags
     * TODO: Eventually use dates to make pretty graph or something
     */

    for (index, line) in reader.lines().enumerate() {
        let line = line
            .unwrap();

        let vec = line
            .split(" ")
            .collect::<Vec<_>>();

        if vec.len() == 0 { continue }

        let x = vec[0]
            .chars()
            .nth(0);

        match x {
            Some('0'..='9') => println!("{}", line),
            _ => continue,
        }
    }
}