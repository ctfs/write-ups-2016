fn hash(data: &[u8]) -> [u8; 8] {
    use std::mem;
    fn b2f64(data: &[u8]) -> f64 {
        let mut buf = [0u8; 8];
        for (i, &x) in data.iter().enumerate().take(8) {
            buf[i] = x;
        }
        (unsafe { mem::transmute::<_, u64>(buf) }) as f64
    }
    
    let r = {
        fn work(data: &[u8]) -> u64 {
            // ???
        }
        
        (0..data.len()).fold(0u64, |x, y| x ^ (work(&data[y..]) as u64))
    };
    
    unsafe { mem::transmute(r) }
}